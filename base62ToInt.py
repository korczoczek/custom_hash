import sys


list="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
def base62ToInt(base62:str) -> int:
    val=0
    multi=1
    for i in base62[::-1]:
        digit=list.find(i)
        if digit == -1:
            raise ValueError("Invalid base62 number")
        val+=digit*multi
        multi*=62
    return val

def main():
    try:
        num=sys.argv[1]
    except:
        print("Provide a valid base62 number")
    
    print(base62ToInt(num))

if __name__=="__main__":
    main()