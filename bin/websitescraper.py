import sys
from pywebcopy import save_website

url = sys.argv[1]
project_folder = sys.argv[2]
project_name = url.split('/')[2]

save_website(
    url=url,
    project_folder=project_folder,
    project_name=project_name,
    bypass_robots=True,
    debug=True,
    open_in_browser=False,
    delay=None,
    threaded=False,
)
