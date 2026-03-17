import hashlib, datetime, json, zipfile, os, uuid
from worlds.Files import APPlayerContainer
from typing import Optional
PASS = "WeDidntSecureThisVeryWell!!1"
INIT = "pemgail9uzpgzl88"
class Byte(object):
    POLY0 = {8,4,3,1,0}
    def _euclide(a: set, b:set):
        q = set()
        r = a
        def deg(s:set):
            if len(s) == 0:
                return 0
            return max(s)
        while deg(r)>=deg(b):
            q_max = deg(r) - deg(b)
            q.add(q_max)
            r ^= {q_max + b0 for b0 in b}
        return r
    def _getL(n: int):
        ret = set()
        for k in range(8, -1, -1):
            if (1<<k) <= n:
                ret.add(k)
                n -= (1<<k)
        return ret
    def to_bytes(self):
        return int(self).to_bytes()
    def __int__(self):
        return sum([1<<k for k in self.L])
    def to_char(self, encoding="utf-8"):
        if encoding == "utf-8":
            return chr(int(self))
        raise NotImplementedError
    def __eq__(self, other):
        if isinstance(other, Byte):
            return self.L == other.L
        if isinstance(other, bytes):
            return int(self) == other[0]
        else:
            return int(self) == int(other)
    def __init__(self, *args):
        if len(args) == 0:
            self.L = {}
        elif isinstance(args[0], int):
            self.L = Byte._getL(args[0])
        elif isinstance(args[0], bytes):
            self.L = Byte._getL(args[0][0])
        elif isinstance(args[0], set):
            self.L = args[0]
        elif isinstance(args[0], str) and len(args[0]) == 1:
            self.L = Byte._getL(ord(args[0]))
        elif isinstance(args[0], str) and len(args[0]) == 2:
            self.L = Byte._getL(int(args[0], 16))
        elif isinstance(args[0], Byte):
            self.L = args[0].L
        else:
            for x in args:
                if not isinstance(x, int):
                    print("Wrong type")
                    assert False
            self.L = set(args)
    def __add__(self, other):
        return Byte(self.L^other.L)
    def __mul__(self, other):
        newL = set()
        for x in self.L:
            newL ^= {x+y for y in other.L}
        r = Byte._euclide(newL, Byte.POLY0)
        return Byte(r)
    def __repr__(self):
        return f"{int(self):02X}"
        
def add_lists(L1, L2):
    return [x + y for (x, y) in zip(L1, L2)]
def reduce(L, t=int):
    if len(L) == 0:
        return t(0)
    if isinstance(L[0], list):
        ret = reduce(L[0], t)
    else:
        t = type(L[0])
        ret = L[0]
    for x in L[1:]:
        if isinstance(x, list):
            ret += reduce(x)
        else:
            ret += x
    return ret
def pbkdf1_ms(f_hash, password, salt, it_idx, dk_len, n=2):
    assert dk_len <= n*20
    word = password+salt
    word = word.encode()
    for _ in range(it_idx-1):
        word = f_hash(word).digest()
    all_words = [f_hash(str(i).encode()+word) if i > 0 else f_hash(word) for i in range(n)]
    L = []
    for word in all_words:
        for s in word.digest():
            L.append(Byte(s))
    return L[:dk_len]
def hex_to_bytes(s:str):
    last = None
    ret = []
    for char in s[::-1]:
        if char == '\t' or char == '\n' or char == ' ':
            continue
        if last is None:
            last = char
        else:
            ret.insert(0, Byte(char+last))
            last=None
    if last is not None:
        ret.insert(0, Byte('0'+last))
    return ret
def to_bytes(obj):
    return [Byte(x) for x in obj]
def get_pass():
    return pbkdf1_ms(hashlib.sha1, PASS, "", 100, 32)
def get_data():
    with open("test.save", "rb") as file:
        return file.read()

class AES(object):

    FORWARD_VALUES = [
        0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
        0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
        0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
        0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
        0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
        0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
        0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
        0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
        0xcd, 0x0c, 0x13 ,0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
        0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
        0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
        0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8 ,0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
        0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
        0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
        0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16 
        ]
    BACKWARD_VALUES = [
        0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb, 
        0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb, 
        0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e, 
        0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25, 
        0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92, 
        0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84, 
        0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06, 
        0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b, 
        0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73, 
        0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e, 
        0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b, 
        0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4, 
        0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f, 
        0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef, 
        0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61, 
        0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
        ]
    def __init__(self, passPhrase):
        self.passPhrase = passPhrase
        assert len(self.passPhrase) == 16 or len(self.passPhrase) == 24 or len(self.passPhrase) == 32
        self.Nk = len(self.passPhrase)//4
        self.Nr = 10 if self.Nk == 4 else 12 if self.Nk == 6 else 14
        self._compute_key_schedule()
    
    def cipher(self, msg: str, initV):
        assert len(initV) == 16
        assert len(msg) > 0
        k_pad = 16 - (len(msg) % 16)
        Lpad = reduce([Byte(k_pad).to_char() for _ in range(k_pad)])
        msg += Lpad
        ret = []
        previous = [Byte(x) for x in initV]
        for k in range(len(msg) // 16):
            curr_block = [Byte(msg[i]) for i in range(16*k, 16*(k+1))]
            msg_cipher = add_lists(curr_block, previous)
            previous = self.cipherBlock(msg_cipher)
            ret.append(previous)
        return [x for L in ret for x in L]
    
    def decipher(self, msg: bytes, initV):
        assert len(initV) == 16
        assert len(msg)%16==0 and len(msg) > 0
        blocks = [[Byte(x) for x in msg[16*k:16*(k+1)]] for k in range(len(msg)//16)]
        deciphered = [self.decipherBlock(block) for block in blocks]
        blocks.insert(0, [Byte(x) for x in initV])
        ret = []
        for k in range(len(deciphered)):
            ret.extend(add_lists(deciphered[k], blocks[k]))
        n_pad = int(ret[-1])
        return reduce([x.to_char() for x in ret[:-n_pad]])

    def decipherBlock(self, msg):
        assert len(msg) == 16
        state = [[0 for _ in range(4)] for _ in range(4)]
        for r in range(4):
            for c in range(4):
                state[r][c] = msg[r + 4*c]
        self._add_round_key(state, self.w, self.Nr*4)
        self._inv_shift_rows(state)
        self._inv_sub_bytes(state)

        for round in range(self.Nr-1, 0, -1):
            self._add_round_key(state, self.w, 4*round)
            self._inv_mix_columns(state)
            self._inv_shift_rows(state)
            self._inv_sub_bytes(state)
        
        self._add_round_key(state, self.w, 0)
        out = [None for _ in range(16)]
        for r in range(4):
            for c in range(4):
                out[r+4*c] = state[r][c]
        return out

    def cipherBlock(self, msg):
        assert len(msg) == 16
        state = [[0 for _ in range(4)] for _ in range(4)]
        for r in range(4):
            for c in range(4):
                state[r][c] = msg[r + 4*c]

        self._add_round_key(state, self.w, 0) 

        for round in range(1, self.Nr):
            self._sub_bytes(state)
            self._shift_rows(state)
            self._mix_columns(state) 
            self._add_round_key(state, self.w, 4*round)

        self._sub_bytes(state)
        self._shift_rows(state)
        self._add_round_key(state, self.w, self.Nr*4)
        out = [None for _ in range(16)]
        for r in range(4):
            for c in range(4):
                out[r+4*c] = state[r][c]
        return out

    def _sub_bytes(self, m):
        for r in range(4):
            for c in range(4):
                m[r][c] = Byte(AES.FORWARD_VALUES[int(m[r][c])])
    def _inv_sub_bytes(self, m):
        for r in range(4):
            for c in range(4):
                m[r][c] = Byte(AES.BACKWARD_VALUES[int(m[r][c])])

    def _shift_rows(self, m):
        for r in range(4):
            m[r] = m[r][r:] + m[r][:r]
    
    def _inv_shift_rows(self, m):
        for r in range(4):
            m[r] = m[r][4-r:] + m[r][:4-r]

    def _mix_columns(self, m):
        for c in range(4):
            vals = [m[r][c] for r in range(4)]
            m[0][c]=(Byte(0x02)*vals[0])+(Byte(0x03)*vals[1])+vals[2]+vals[3]
            m[1][c]=vals[0]+(Byte(0x02)*vals[1])+(Byte(0x03)*vals[2])+vals[3]
            m[2][c]=vals[0]+vals[1]+(Byte(0x02)*vals[2])+(Byte(0x03)*vals[3])
            m[3][c]=(Byte(0x03)*vals[0])+vals[1]+vals[2]+(Byte(0x02)*vals[3])
        
    def _inv_mix_columns(self, m):
        for c in range(4):
            vals = [m[r][c] for r in range(4)]
            m[0][c]=(Byte(0x0e)*vals[0])+(Byte(0x0b)*vals[1])+(Byte(0x0d)*vals[2])+(Byte(0x09)*vals[3])
            m[1][c]=(Byte(0x09)*vals[0])+(Byte(0x0e)*vals[1])+(Byte(0x0b)*vals[2])+(Byte(0x0d)*vals[3])
            m[2][c]=(Byte(0x0d)*vals[0])+(Byte(0x09)*vals[1])+(Byte(0x0e)*vals[2])+(Byte(0x0b)*vals[3])
            m[3][c]=(Byte(0x0b)*vals[0])+(Byte(0x0d)*vals[1])+(Byte(0x09)*vals[2])+(Byte(0x0e)*vals[3])

    def _add_round_key(self, m, W, k):
        for c in range(4):
            L = add_lists([m[r][c] for r in range(4)], W[k+c])
            for r in range(4):
                m[r][c] = L[r]

    def _sub_word(self, w):
        return [Byte(AES.FORWARD_VALUES[int(w[i])]) for i in range(4)]
    
    
    def _rot_word(self, w):
        return [w[1], w[2], w[3], w[0]]
    
    def _rcon(self, i):
        return [Byte({i-1}), Byte(0), Byte(0), Byte(0)]
    
    def _compute_key_schedule(self):
        self.w=[[Byte(self.passPhrase[4*i]), Byte(self.passPhrase[4*i+1]), Byte(self.passPhrase[4*i+2]), Byte(self.passPhrase[4*i+3])] for i in range(self.Nk)]
        for i in range(self.Nk, 4*(self.Nr+1)):
            tmp = self.w[-1]
            if (i%self.Nk==0):
                tmp = add_lists(self._sub_word(self._rot_word(tmp)), self._rcon(i//self.Nk))
            elif (self.Nk > 6 and i%self.Nk == 4):
                tmp = self._sub_word(tmp)
            self.w.append(add_lists(self.w[i-self.Nk], tmp))


def int_to_int64(n: int):
    return [n & 0xff, (n & 0xff00) >> 8, (n & 0xff0000) >> 16, (n & 0xff000000) >> 24, (n & 0xff00000000) >> 32, (n & 0xff0000000000) >> 40, (n & 0xff000000000000) >> 48, (n & 0xff00000000000000) >> 56]
def int64_to_int(L):
    n = 0
    for i, k in enumerate(L):
        n += k*(1<<(8*i))
    return n
class PakyIn(object):
    def __init__(self, filename):
        with open(filename, "rb") as f:
            L = f.read()
        n = L[14]
        self.data = {}
        for k in range(n):
            t = int64_to_int(L[18+20*k:22+20*k])
            x_start = int64_to_int(L[22+20*k:30+20*k])
            x_end = int64_to_int(L[30+20*k:38+20*k])
            self.data[t] = L[x_start:x_end]
class Paky(object):
    def __init__(self, filename):
        self.chunks = []
        self.name = filename
    
    def add_chunk(self, t: int, data):
        self.chunks.append((t, data))
        
    def write(self):
        header = [
            'P', 'A', 'K', 'Y', 0,
            'S', 'A', 'V', 'E', 0,
            1, 0, 1, 0, # Versions, maybe need to change when update
            len(self.chunks), 0, 0, 0 # Nb of chunks
        ]
        curr_idx = len(header)+20*len(self.chunks)+1
        for (t, data) in self.chunks:
            header.extend([
                t, 0, 0, 0 #Type of the chunk, simplification if t<256 which it should be
            ] + int_to_int64(curr_idx) #Start of chunk in file
              + int_to_int64(curr_idx+len(data)) #End of chunk in file
            )
            curr_idx += len(data)
        header.append(0)
        for (_, data) in self.chunks:
            header.extend(data)
        
        return bytes([int(Byte(x)) for x in header])
    
    def write_to_file(self, filename=None):
        if filename is None:
            if self.name is None:
                raise ValueError("Please provide a filename")
            filename = self.name
        with open(filename, "wb") as f:
            f.write(self.write())

def create_save(world, filename):
    now = datetime.datetime.now().astimezone()
    offset = now.tzinfo.utcoffset(None).seconds
    sign = '+' if offset >= 0 else '-'
    p_pos = []
    timestamp = f"{now.year:04}-{now.month:02}-{now.day:02}T{now.hour:02}:{now.minute:02}:{now.second:02}.0000000{sign}{abs(offset)//3600:02}:00"
    data_info = {
        "Timestamp": timestamp,
        "Type": "Manual",
        "Name": f"{now.year:04}-{now.month:02}-{now.day:02} {now.hour:02}:{now.minute:02}:{now.second:02}",
        "World": "World1",
        "GameMode": "Career",
        "DataVersion": 1
    }
    data_dict = get_data(now, world)
    paky = Paky(filename)
    json_info = json.dumps(data_info)
    paky.add_chunk(2, [Byte(x) for x in json_info])
    json_data = json.dumps(data_dict)
    cryptObj = AES(get_pass())
    ciphered_data = cryptObj.cipher(json_data, INIT)
    paky.add_chunk(1, ciphered_data)
    paky.add_chunk(25, [Byte(x) for x in json_data])
    return paky
station_positions = [
    ({"x":15596.2, "y":204.3, "z":11134.0}, {"x":0.0, "y":0.7 , "z":0.0, "w":-0.7}),
    ({"x":8475.5, "y": 156.4, "z":3476.2}, {"x":0.0, "y": 0.0, "z":0.0, "w":1.0}),
    ({"x":2104.5, "y":145.1, "z":8991.6}, {"x":0.0, "y": 0.8, "z":0.0, "w":-0.5}),
    ({"x":9948.7, "y": 134.7, "z":1344.6}, {"x":0.0, "y": 1.0, "z":0.0, "w":0.0}),
    ({"x":2019.7, "y":122.2, "z":5678.8}, {"x":0.0, "y": 0.9, "z":0.0, "w":0.4}),
    ({"x":9479.3, "y":119.3, "z":13615.4}, {"x":0.0, "y": 0.8, "z":0.0, "w":-0.6}),
    ({"x":5998.2, "y":124.0, "z":6741.1}, {"x":0.0, "y": 0.5, "z":0.0, "w":-0.9}),
    ({"x":5688.7, "y":144.9, "z":8698.4}, {"x":0.0, "y": 1.0, "z":0.0, "w":-0.2}),
    ({"x":5357.5, "y": 174.7, "z":3710.2}, {"x":0.0, "y": 0.7, "z":0.0, "w":0.8}),
    ({"x":12852.3, "y": 140.2, "z":11037.2}, {"x":0.0, "y": 0.2, "z":0.0, "w":-1.0}),
    ({"x":13063.0, "y": 113.1, "z":3530.3}, {"x":0.0, "y": 1.0, "z":0.0, "w":-0.2}),
    ({"x":14958.3, "y":248.2, "z":15248.7}, {"x":0.0, "y": 0.6, "z":0.0, "w":-0.8}),
    ({"x":2025.2, "y":133.5, "z":13401.8}, {"x":0.0, "y": 0.5, "z":0.0, "w":-0.8}),
    ({"x":12762.7, "y":215.1, "z":14759.1}, {"x":0.0, "y": 0.8, "z":0.0, "w":-0.6}),
    ({"x":2354.0, "y":159.3, "z":10972.0}, {"x":0.0, "y": 0.7, "z":0.0, "w":-0.7}),
    ({"x":6386.8, "y":143.9, "z":11308.6}, {"x":0.0, "y": 0.8, "z":0.0, "w":0.6}),
    ({"x":4952.2, "y":123.1, "z":6275.0}, {"x":0.0, "y": 1.0, "z":0.0, "w":0.0}),
    ({"x":11548.6, "y":122.3, "z":11528.7}, {"x":0.0, "y": 1.0, "z":0.0, "w":0.3}),
    ({"x":512.6, "y": 131.9, "z":760.5}, {"x":0.0, "y": 0.9, "z":0.0, "w":0.4}),
    ({"x":7919, "y": 131.9, "z":7345.5}, {"x":0.0, "y": 0.9, "z":0.0, "w":0.4})
    ]

def get_data(now, world):
    offset = now.tzinfo.utcoffset(None).seconds
    sign = '+' if offset >= 0 else '-'
    timestamp = f"{now.year:04}-{now.month:02}-{now.day:02}T{now.hour:02}:{now.minute:02}:{now.second:02}.0000000{sign}{abs(offset)//3600:02}:00"
    data_dict = {
        "Version": 8,
        "Version_initial": 8,
        "Game_version_initial": "Build 99 - steam",
        "Game_version_latest": "Build 99 - steam",
        "Game_mode": "Career",
        "World": "World1",
        "Starting_time_and_date": 0, 
        "Licenses_General": [],
        "Licenses_Job": [],
        "Player_money": world.options.money.value,
        "Tutorial_01_completed": True,
        "Tutorial_02_completed": True,
        "Tutorial_03_completed": True,
        "Starting_items": 0, 
        "ModManagers": {
            "modManagerName": "UnityModManager",
            "modManagerVersion": "0.32.4.0",
            "timestamp": timestamp+'Z',
            "harmonyVersion": "2.3.6.0",
            "loadedMods": [{
                "name": "Randomizer",
                "version": "0.1.0",
                "timestamp": timestamp+'Z'
            }]
        },
        "Player_position": station_positions[world.starting_station][0], 
        "Player_rotation": station_positions[world.starting_station][1],
        "Player_car_guid": "",
        "Garages": [],
        "RandoData": {
            "StationLicenses": [False for _ in range(20)],
            "HiddenGarages": [False for _ in range(4)],
            "JobLocations": [False for _ in range(12)],
            "GeneralLocations": [False for _ in range(12)],
            "LocoLocations": [False for _ in range(57)],
            "Index": [0],
            "ReceivedRelics": [0 for _ in range(6)],
            "Shunts": [0 for _ in range(20)],
            "ShuntThreshold": [world.options.nb_shunts.value for _ in range(20)],
            "Freights": [0 for _ in range(20)],
            "FreightThreshold": [world.options.nb_freights.value for _ in range(20)],
            "LocoJobs": [0 for _ in range(6)],
            "LocoJobsThreshold": [world.options.nb_locos.value for _ in range(6)],
            "Victory": world.options.nb_stations.value,
            "VictoryThreshold": world.options.nb_jobs.value,
            "AlreadyWon": False,
            "Version": 1,
            "IsFirstLoading": True,
        },
        "Storage_Inventory": [
            {"itemPrefabName":"CommsRadio",
            "itemPositionX":0.0,
            "itemPositionY":0.0,
            "itemPositionZ":0.0,
            "itemRotationX":0.0,
            "itemRotationY":0.0,
            "itemRotationZ":0.0,
            "itemRotationW":0.0,
            "belongsToPlayer":True,
            "isGrabbed":False,
            "inventorySlotIndex":0,
            "containerSlotIndex":-1,
            "inLockedSlot":False,
            "isDropped":False,
            "carGuid":None,
            "containerId":None,
            "state":{},
            "ItemPosition":{"x":0.0,"y":0.0,"z":0.0},
            "ItemRotation":{"x":0.0,"y":0.0,"z":0.0,"w":0.0}},

            {"itemPrefabName":"Map",
            "itemPositionX":0.0,
            "itemPositionY":0.0,
            "itemPositionZ":0.0,
            "itemRotationX":0.0,
            "itemRotationY":0.0,
            "itemRotationZ":0.0,
            "itemRotationW":0.0,
            "belongsToPlayer":True,
            "isGrabbed":False,
            "inventorySlotIndex":1,
            "containerSlotIndex":-1,
            "inLockedSlot":False,
            "isDropped":False,
            "carGuid":None,
            "containerId":None,
            "state":{},
            "ItemPosition":{"x":0.0,"y":0.0,"z":0.0},
            "ItemRotation":{"x":0.0,"y":0.0,"z":0.0,"w":0.0}},

            {"itemPrefabName":"MapSchematic",
            "itemPositionX":0.0,
            "itemPositionY":0.0,
            "itemPositionZ":0.0,
            "itemRotationX":0.0,
            "itemRotationY":0.0,
            "itemRotationZ":0.0,
            "itemRotationW":0.0,
            "belongsToPlayer":True,
            "isGrabbed":False,
            "inventorySlotIndex":2,
            "containerSlotIndex":-1,
            "inLockedSlot":False,
            "isDropped":False,
            "carGuid":None,
            "containerId":None,
            "state":{},
            "ItemPosition":{"x":0.0,"y":0.0,"z":0.0},
            "ItemRotation":{"x":0.0,"y":0.0,"z":0.0,"w":0.0}},
            
            {"itemPrefabName":"RouteMap",
            "itemPositionX":0.0,
            "itemPositionY":0.0,
            "itemPositionZ":0.0,
            "itemRotationX":0.0,
            "itemRotationY":0.0,
            "itemRotationZ":0.0,
            "itemRotationW":0.0,
            "belongsToPlayer":True,
            "isGrabbed":False,
            "inventorySlotIndex":3,
            "containerSlotIndex":-1,
            "inLockedSlot":False,
            "isDropped":False,
            "carGuid":None,
            "containerId":None,
            "state":{},
            "ItemPosition":{"x":0.0,"y":0.0,"z":0.0},
            "ItemRotation":{"x":0.0,"y":0.0,"z":0.0,"w":0.0}},
            
            {"itemPrefabName":"wallet",
            "itemPositionX":0.0,
            "itemPositionY":0.0,
            "itemPositionZ":0.0,
            "itemRotationX":0.0,
            "itemRotationY":0.0,
            "itemRotationZ":0.0,
            "itemRotationW":0.0,
            "belongsToPlayer":True,
            "isGrabbed":False,
            "inventorySlotIndex":11,
            "containerSlotIndex":-1,
            "inLockedSlot":False,
            "isDropped":False,
            "carGuid":None,
            "containerId":None,
            "state":{},
            "ItemPosition":{"x":0.0,"y":0.0,"z":0.0},
            "ItemRotation":{"x":0.0,"y":0.0,"z":0.0,"w":0.0}},
            
            {"itemPrefabName":"VehicleCatalog",
            "itemPositionX":0.0,
            "itemPositionY":0.0,
            "itemPositionZ":0.0,
            "itemRotationX":0.0,
            "itemRotationY":0.0,
            "itemRotationZ":0.0,
            "itemRotationW":0.0,
            "belongsToPlayer":True,
            "isGrabbed":False,
            "inventorySlotIndex":12,
            "containerSlotIndex":-1,
            "inLockedSlot":False,
            "isDropped":False,
            "carGuid":None,
            "containerId":None,
            "state":{},
            "ItemPosition":{"x":0.0,"y":0.0,"z":0.0},
            "ItemRotation":{"x":0.0,"y":0.0,"z":0.0,"w":0.0}},
            
            {"itemPrefabName":"Compass",
            "itemPositionX":0.0,
            "itemPositionY":0.0,
            "itemPositionZ":0.0,
            "itemRotationX":0.0,
            "itemRotationY":0.0,
            "itemRotationZ":0.0,
            "itemRotationW":0.0,
            "belongsToPlayer":True,
            "isGrabbed":False,
            "inventorySlotIndex":13,
            "containerSlotIndex":-1,
            "inLockedSlot":False,
            "isDropped":False,
            "carGuid":None,
            "containerId":None,
            "state":{},
            "ItemPosition":{"x":0.0,"y":0.0,"z":0.0},
            "ItemRotation":{"x":0.0,"y":0.0,"z":0.0,"w":0.0}},
            
        ],
        "Storage_World": [],
        'Storage_LostAndFound': [
        ],
        'Storage_InstalledGadgets': [], 
        'Storage_ItemContainers': [], 
        'Turntables':{
            "T_SW_1": {"rot": 0.0},
            "T_FRS_1": {"rot": 0.0},
            "T_MB_1": {"rot": 0.0},
            "T_OWC_1": {"rot": 0.0},
            "T_IMW_1": {"rot": 0.0},
            "T-CS-1": {"rot": 0.0},
            "T_MF_1": {"rot": 0.0},
            "T_HB_1": {"rot": 0.0},
            "T_CW_1": {"rot": 0.0},
            "T_SM_1": {"rot": 0.0},
            "T_FF_1": {"rot": 0.0}
        }, 
        'Unique_cars': {}, 
        'Customizers': {"holes": []}, 
        'Caboose_In_Range': False, 
        'Debt_existing_locos': [], 
        'Debt_deleted_locos': [], 
        'Debt_existing_jobs': [], 
        'Debt_staged_jobs': [], 
        'Debt_existing_jobless_cars': None, 
        'Debt_deleted_jobless_cars': {"d": [], "t": 0.0}, 
        'Debt_insurance': {"paid": 0.0},
        'Debt_deleted_owned_cars': [], 
        'Debt_total': 0.0, 
        'Time_and_date': {"OADate": 0.0, "WeatherOffset": 0.0, "Wetness": 0.0}, 
        'Last_wake_time': 0.0, 
        'Last_sleep_duration': 0, 
        'DataVersion': 21,
    }
    return data_dict

class DVPatch(APPlayerContainer):
    game = "Derail Valley"
    patch_file_ending = ".save"

    def __init__(self, world: "DVWorld", filename: str="", output_directory: str="", player: Optional[int]=0, player_name: str="", server: str = ""):
        self.filename = filename
        self.paky = create_save(world, self.filename)
        container_path=os.path.join(output_directory, self.filename)
        super().__init__(container_path, player, player_name, server)
    
    def write_contents(self, opened_zipfile: zipfile.ZipFile):
        opened_zipfile.writestr(self.paky.name, self.paky.write())
        super().write_contents(opened_zipfile)
        