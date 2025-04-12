from pyodide.http import pyfetch # type: ignore
import asyncio

__doc__ = '''
實際業務邏輯
'''

def main():
    # 全局變量
    class glo:
        csv_text = ''
    # 加載csv
    async def load_csv():
        response = await pyfetch('data.csv')
        glo.csv_text = await response.text()
    asyncio.ensure_future(load_csv())
    # 緩存ui對象
    txt_output = get_by_id('txt_output')
    user_input = get_by_id('user_input')
    btn_analyse = get_by_id('btn_analyse')
    # 綁定按鈕
    def on_click(event):
        if glo.csv_text == '':
            result = '數據尚未加載完成，請稍候'
        else:
            result = analyze_csv(glo.csv_text, user_input.value)
        txt_output.innerHTML = result
    bind_click_event(btn_analyse, on_click)
    # 綁定回車
    def on_keypress(event):
        if event.key == 'Enter':
            on_click(event)
    bind_event(user_input, 'keypress', on_keypress)
main()

if __name__ == "__main__":
    # 假import，僅用於編譯器顯示懸停提示
    try:
        from pyodide_tools import *
        from analysis import *
    except:
        pass