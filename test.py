import time
from console_progressbar import ProgressBar

pb = ProgressBar(total=10, prefix='Here', suffix='Now', decimals=0, length=50, fill='X', zfill='-')
for i in range(10):
    pb.print_progress_bar(i)
    time.sleep(1)