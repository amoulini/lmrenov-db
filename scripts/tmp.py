def test(raising: bool = True):
    try:
        if raising:
            print("Raising exception")
            raise Exception("Testing error")
        else:
            print("Not raising exception")
            return 1
        
    except:
        print("The exception was caught")
        return 0
    
    finally:
        print("Finally block")


if __name__ == "__main__":
    res = test(True)
    print(f"result is {res}")
    print()

    res = test(False)
    print(f"result is {res}")