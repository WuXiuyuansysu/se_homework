from classes.class_user import User
import json

class login:
    """
    用户登录管理类，负责用户的注册、认证和用户信息加载。

    属性:
        success (bool): 登录状态，指示当前是否成功登录，初始为 False。
        username (str or None): 当前登录用户名，初始为 None。
        User (User or None): 当前登录用户的 User 对象实例，初始为 None。

    方法:
        load_user(username: str) -> bool:
            根据用户名加载用户信息，创建 User 实例。

        authenticate(username: str, password: str) -> bool:
            验证用户名和密码是否正确，成功则加载用户信息。

        register(username: str, password: str) -> bool:
            注册新用户，创建用户文件夹及相关数据结构。
    """
    def __init__(self):
        """
        初始化登录类实例，设置默认状态：
        - success: 登录状态，初始为 False
        - username: 当前用户名，初始为 None
        - User: 用户对象实例，初始为 None
        """
        self.success = False
        self.username = None
        self.User = None

    def load_user(self, username):
        """
        根据用户名加载用户信息，创建 User 实例。

        参数：
            username (str): 用户名

        返回：
            bool: 如果成功创建用户实例返回 True，否则返回 False
        """
        self.username = username
        self.User = User(username)
        if not self.User:
            return False
        
        return True

    def authenticate(self, username, password):
        """
        验证用户名和密码是否正确。

        过程：
        - 从 ./data/user_table.json 文件中加载用户数据。
        - 检查是否有用户名和密码匹配的用户。
        - 匹配成功后调用 load_user 加载用户信息。

        参数：
            username (str): 用户名
            password (str): 密码

        返回：
            bool: 认证成功返回 True，失败返回 False。
        """
        #从./data/user_table.json中加载用户数据
        try:
            with open("./data/user_table.json", "r", encoding="utf-8") as f:
                user_table = json.load(f)
        except FileNotFoundError:
            return False
        
        #检查用户名和密码是否匹配
        for user in user_table:
            if user['username'] == username and user['password'] == password:
                self.load_user(user['username'])
                return True
        return False

        
    def register(self, username, password):
        """
        注册新用户。

        过程：
        - 从 ./data/user_table.json 文件中加载现有用户数据。
        - 检查用户名是否已存在，存在则返回 False。
        - 添加新用户信息，保存回文件。
        - 创建用户文件夹及相关子文件夹（收藏、历史记录）。
        - 初始化 User 实例。

        参数：
            username (str): 新用户名
            password (str): 密码

        返回：
            bool: 注册成功返回 True，失败返回 False。
        """
        #从./data/user_table.json中加载用户数据
        try:
            with open("./data/user_table.json", "r", encoding="utf-8") as f:
                user_table = json.load(f)
        except FileNotFoundError:
            user_table = []
        #检查用户名是否已存在
        for user in user_table:
            if user['username'] == username:
                return False
        #添加新用户到用户表
        new_user = {
            "username": username,
            "password": password
        }
        user_table.append(new_user)

        #保存用户表到文件
        with open("./data/user_table.json", "w", encoding="utf-8") as f:
            json.dump(user_table, f, ensure_ascii=False, indent=4)
        
        #创建用户文件夹以及下面的收藏文件夹和历史记录文件夹
        self.username = username
        self.User = User(self.username)
        self.User.setup()

        return True

#测试
if __name__ == "__main__":
    login_instance = login()
    username = "testuser"
    password = "testpassword"

    # 注册新用户
    if login_instance.register(username, password):
        print(f"用户 {username} 注册成功！")
    else:
        print(f"用户 {username} 注册失败，可能用户名已存在。")

    # 验证用户登录
    if login_instance.authenticate(username, password):
        print(f"用户 {username} 登录成功！")
    else:
        print(f"用户 {username} 登录失败，用户名或密码错误。")