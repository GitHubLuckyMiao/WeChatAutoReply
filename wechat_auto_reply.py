from itchat.content import *
import itchat
import time
import os

# 设置全局变量
MY_NICKNAME = ""  # 设置为你的微信昵称
AUTO_REPLY = "[自动回复]\n你好, 本人白天暂时外出, 有事请留言, 晚上回来处理, 谢谢😄"


def mkdir(path):
    try:
        folder = os.path.exists(path)
        if not folder:
            os.makedirs(path)
    except Exception:
        pass


# 有备注名则返回备注名, 否则返回昵称
def get_name(msg):
    if msg["User"]["RemarkName"] != "":
        return msg["User"]["RemarkName"]
    else:
        return msg["User"]["NickName"]


def is_from_myself(msg):
    itchat.get_friends(update=True)
    myself = itchat.search_friends(nickName=str(MY_NICKNAME))[0]
    return msg['FromUserName'] == myself['UserName']


# 对于一般内容的自动回复
@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING], isFriendChat=True)
def text_reply(msg):
    name = get_name(msg)
    if not is_from_myself(msg):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
              " 收到来自-> " + name + " <-的消息: \"" + msg.text + "\"")
        msg.user.send(AUTO_REPLY)


# 对于文件内容的保存与自动回复
@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True)
def download_files(msg):
    name = get_name(msg)
    mkdir(name)
    msg.download("./" + name + "/" + msg.fileName)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
          " 收到来自-> " + name + " <-的文件, 并保存为-> ./" + name + "/" + msg.fileName)
    return AUTO_REPLY


# 对于群消息中@本人的自动回复
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg.isAt:
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
              " 收到来自" + msg.ActualNickName + " <-的群中@消息: \"" + msg.text + "\"")
        msg.user.send(u'@%s\n%s' % (msg.ActualNickName, AUTO_REPLY))


# 对于好友请求的自动同意
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    msg.user.verify()
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
          " 收到来自-> " + get_name(msg) + " <-的好友添加请求, 已默认通过")
    msg.user.send("Hi😁nice 2 meet U!\n" + AUTO_REPLY)


if __name__ == '__main__':
    itchat.auto_login(hotReload=True)  # cli终端登录则需设置enableCmdQR=True, 具体请查文档
    itchat.dump_login_status()
    itchat.run()
    itchat.dump_login_status()
