from js import document # type: ignore
from pyodide.ffi import create_proxy # type: ignore
import asyncio

__doc__ = '''
pyodide封裝的一些工具
'''

def get_by_id(id):
    '''
    根據html中的id獲取對象
    '''
    return document.getElementById(id)

def create_text(
    text : str,
    text_id : str = None,
    is_append : bool = True,
) -> object:
    '''
    創建文本
    '''
    div = document.createElement('div')
    div.innerHTML = text
    if text_id:
        div.id = text_id
    if is_append:
        document.body.appendChild(div)
    else:
        document.body.prepend(div)

def create_button(text: str, parent_id: str = "body", button_id: str = None) -> dict:
    """
    极简按钮创建方法

    :param text: 按钮显示文本
    :param parent_id: 父容器ID (默认body)
    :param button_id: 按钮自定义ID
    :return: 包含元素的字典 {'element': button, 'remove': cleanup_func}
    """
    parent = document.body if parent_id == 'body' else document.getElementById(parent_id)
    if not parent:
        raise ValueError(f"Parent container #{parent_id} not found")

    btn = document.createElement("button")
    btn.innerHTML = text
    if button_id:
        btn.id = button_id
        
    parent.appendChild(btn)
    return {"element": btn, "remove": lambda: btn.remove()}

def bind_event(element, event_type: str, callback, async_callback: bool = False) -> callable:
    """
    通用事件绑定方法

    :param element: DOM元素
    :param event_type: 事件类型（如 'click'）
    :param callback: 回调函数
    :param async_callback: 是否异步执行
    :return: 清理函数（解除绑定）
    """
    def handler_wrapper(event):
        try:
            if async_callback:
                future = asyncio.ensure_future(callback(event))
                future.add_done_callback(lambda f: f.exception() and None)
            else:
                callback(event)
        except Exception as e:
            print(f"Event error: {str(e)}")

    proxy = create_proxy(handler_wrapper)
    element.addEventListener(event_type, proxy)
    
    def cleanup():
        element.removeEventListener(event_type, proxy)
        proxy.destroy()
    
    return cleanup

def bind_click_event(element, callback, async_callback: bool = False) -> callable:
    '''
    綁定點擊事件

    :param element: DOM元素
    :param callback: 回调函数
    :param async_callback: 是否异步执行
    :return: 清理函数（解除绑定）
    '''
    return bind_event(element, 'click', callback, async_callback)

# def create_button(
#     text: str,
#     callback,
#     parent_id: str = "body",
#     button_id: str = None,
#     styles: dict = None,
#     classes: list = None,
#     async_callback: bool = False
# ) -> object:
#     """
#     通用按钮创建与事件绑定方法
    
#     参数:
#     text: 按钮显示文本
#     callback: 点击回调函数(支持普通函数/协程)
#     parent_id: 父容器ID (默认body)
#     button_id: 按钮自定义ID
#     styles: CSS样式字典 {'color': 'red', ...}
#     classes: CSS类列表 ['btn', 'primary']
#     async_callback: 是否异步回调
#     """
#     # 获取父容器
#     if parent_id == 'body':
#         parent = document.body
#     else:
#         parent = document.getElementById(parent_id)
#         if not parent:
#             raise ValueError(f"Parent container #{parent_id} not found")

#     # 创建按钮元素
#     btn = document.createElement("button")
#     btn.innerHTML = text

#     # 设置属性
#     if button_id:
#         btn.id = button_id
#     if classes:
#         btn.className = " ".join(classes)
#     if styles:
#         for prop, value in styles.items():
#             btn.style.setProperty(prop, value)

#     # 包装回调函数
#     def callback_wrapper(event):
#         try:
#             if async_callback:
#                 # 异步回调处理
#                 future = asyncio.ensure_future(callback(event))
#                 future.add_done_callback(
#                     lambda f: console.log("Async callback completed") if f.exception() is None else None
#                 )
#             else:
#                 # 同步回调
#                 result = callback(event)
#                 if asyncio.iscoroutine(result):
#                     raise TypeError("同步模式下不能使用协程函数，请设置 async_callback=True")
#         except Exception as e:
#             console.error(f"Callback error: {str(e)}")

#     # 绑定事件（使用Proxy防止内存泄漏）
#     proxy = create_proxy(callback_wrapper)
#     btn.addEventListener("click", proxy)

#     # 添加到父容器
#     parent.appendChild(btn)

#     # 返回按钮引用及清理方法
#     return {
#         "element": btn,
#         "remove": lambda: clean_up(btn, proxy)
#     }

# def clean_up(btn, proxy):
#     """清理事件监听器"""
#     btn.removeEventListener("click", proxy)
#     proxy.destroy()


# # 同步回调示例
# def sync_click(event):
#     document.getElementById("output").innerHTML += "同步点击! "

# create_button(
#     text="同步按钮",
#     callback=sync_click,
#     # parent_id="toolbar",
#     styles={"background": "#4CAF50", "color": "white"},
#     classes=["btn", "rounded"]
# )

# # 异步回调示例
# async def async_click(event):
#     await asyncio.sleep(1)
#     document.getElementById("output").innerHTML += "异步响应! "

# create_button(
#     text="异步按钮",
#     callback=async_click,
#     # parent_id="toolbar",
#     async_callback=True,
#     styles={"background": "#2196F3", "color": "white"}
# )

# # 带清理的复杂示例
# button_data = create_button(
#     text="临时按钮",
#     callback=lambda e: print("临时按钮点击"),
#     button_id="temp-btn"
# )

# # 5秒后移除按钮
# def remove_temp():
#     button_data["remove"]()
#     document.getElementById("temp-btn").remove()

# asyncio.get_event_loop().call_later(5, remove_temp)