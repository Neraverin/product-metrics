# This is a sample Python script.
from wallarm_api import WallarmAPI


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    api = WallarmAPI()
    api.client_id()
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
