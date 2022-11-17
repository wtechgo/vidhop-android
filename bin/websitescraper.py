import sys
from pywebcopy import save_website

url = sys.argv[1]
websites_dir = sys.argv[2]

name = url.split('/')[3].split('?')[0]  # selects first segment after the domain, throws away query parameters.
project_folder = f"{websites_dir}/{name}"
project_name = 'site'

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
