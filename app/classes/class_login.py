from classes.class_user import User
import json

class login:
    def __init__(self):
        self.success = False
        self.username = None
        self.User = None

    def load_user(self, username):
        """
        根据用户名和密码加载用户信息
        """
        self.username = username
        self.User = User(username)
        if not self.User:
            return False
        
        return True

    def authenticate(self, username, password):
        """
        验证用户名和密码是否正确
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
        注册新用户
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