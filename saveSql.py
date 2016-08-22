"""saveSql

Usage: saveSql [-cxj] <dir> <db>

Options:
    -h,--help       显示帮助菜单
    -c              csv格式文件
    -x              excel格式文件
    -j              json格式文件

Example:
    python saveSql.py -c data s_company     将目录data下的csv格式文件存入表s_company中
"""

from docopt import docopt
from insertData import insertData
import time


def cli():
    kwargs = docopt(__doc__)
    insertData(**kwargs)


if __name__ == "__main__":
    start = time.time()
    cli()
    end = time.time()
    print("time: %s" % (end - start))
