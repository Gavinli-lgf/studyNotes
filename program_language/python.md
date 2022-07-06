# 
## argparse
* 新建argparse对象，并增加该脚本的帮助信息“-h”或者“--help”
    parser = argparse.ArgumentParser(
        description='Process and analyze control and planning data')
    parser.add_argument('--bag', type=str, help='use bag')
    parser.add_argument('--path', type=str, help='path for bag files')
* The parse_args() method
  Convert argument strings to objects and assign them as attributes of the namespace. Return the populated namespace.
* 
