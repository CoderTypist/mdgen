from mdgen import mdgen

def main():
    mdgen('testfile.py', out='testfile.md')
    mdgen('mdgen.py', out='mdgen.md')

if __name__ == '__main__':
    main()
    