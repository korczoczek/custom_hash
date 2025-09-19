import hashlib
import sys
import argparse
import time

def help():
    print(f"\nUsage:\npython {sys.argv[0]} start pattern [index (base62)]")

def getAddon(num:int,div:int,list:str) -> str:
    addon=""
    if num == 0:
        addon="0"
    else:
        while num>0:
            remainder=num%div
            addon=f"{list[remainder]}{addon}"
            num-=remainder
            num= num//div
    return addon

def charStartCount(str:str,char:str) -> int:
    count=0
    #char=char[0]
    length=len(char)
    for i,c in enumerate(str):
        if c!=char[i%length]:
            break
        count+=1
    return count

def charScatterCount(str:str,char:str) -> int:
    count=0
    char_len=len(char)
    for i in range(len(str)-(char_len-1)):
        if str[i]==char[0]:
            if charStartCount(str[i:i+char_len],char)==char_len:
                count+=1
    return count

def baseXToInt(baseX:str,list:str) -> int:
    val=0
    multi=1
    count=len(list)
    for i in baseX[::-1]:
        digit=list.find(i)
        if digit == -1:
            raise ValueError("Invalid base62 number")
        val+=digit*multi
        multi*=count
    return val

def isHex(text:str) -> bool:
    hex="0123456789abcdef"
    for i in text:
        if hex.count(i)==0:
            return False
    return True

if __name__ == "__main__":
    parser=argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s","--scatter",action="store_true",help="Find as many instances of the given key scattered through the string, instead of just at the beginning")
    parser.add_argument("-a","--all",action="store_true",help="Find as many examples at the current depth")
    parser.add_argument("-c","--count",action="store",type=int,nargs="?",default=1,help="Starting count")
    parser.add_argument('message', metavar="message",type=str,nargs="?",default="",help="Starting content of the message")
    parser.add_argument("key",metavar="key",type=str,nargs="?",default="0",help="Key to be found in the resulting hash")
    parser.add_argument("index",metavar="index",type=str,nargs="?",default="0",help="Starting index of the search in base62")

    args=parser.parse_args()


    list="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    divider=len(list)
    message=args.message
    key=args.key
    if isHex(key)==0:
        print("Key must be a valid hexadecimal value")
        exit()
    try:
        i=baseXToInt(args.index,list)
    except ValueError:
        print("Start index must be a valid base62 integer")
        exit()

    if message=="":
        sep=""
    else:
        sep=" "
    
    max=args.count

    if not args.all:
        max-=1

    if max<0:
        max=0
    

    curr=time.time()
    
    try:
        while True:
            hex_init=f"{message}{sep}{getAddon(i,divider,list)}"
            if time.time()-curr>1:
                print(f"\r{hex_init}",end=" ")
                curr=time.time()
            hex=hashlib.sha256(hex_init.encode()).hexdigest()
            if args.scatter:
                count=charScatterCount(hex,key)
            else:
                if hex.startswith(key[0]):
                    count=charStartCount(hex,key)
                else:
                    count=0
            if (count>=max and args.all) or ((count>max and not args.all)):
                max=count
                if args.scatter:
                    print(f"\rFound sha256 hash with {max} instances of key \"{key}\"")
                else:
                    print(f"\rFound sha256 hash starting with \"{hex[:max]}\" ({max} characters):")
                print(hex_init)
                print(hex)
            i+=1
    except KeyboardInterrupt as e:
        print(f"\n{e}")