import tkinter as tk
from tkinter import ttk
import pymysql
from tkinter import StringVar

# 初始化訂單字典
order_dict = {}

def add_item(item, price):
    if item in order_dict:
        order_dict[item]['quantity'] += 1
        order_dict[item]['total'] += price
    else:
        order_dict[item] = {'price': price, 'quantity': 1, 'total': price}
    update_treeview()
    print(order_dict)

def remove_item(item, price):
    if item in order_dict and order_dict[item]['quantity'] > 0:
        order_dict[item]['quantity'] -= 1
        order_dict[item]['total'] -= price
        if order_dict[item]['quantity'] == 0:
            del order_dict[item]
        update_treeview()
        print(order_dict)

def update_treeview():
    for row in treeview.get_children():
        treeview.delete(row)
    
    for item, info in order_dict.items():
        treeview.insert("", "end", values=(item, info['price'], info['quantity'], info['total']))


def total():
    total_cost = 0
    for item, info in order_dict.items():
        total_cost += info['total']
    
    total_value.set(f"{total_cost} 元")


def clear_list():
    total_value.set('')  # 清空總金額顯示
    order_dict.clear()   # 清空訂單字典
    # 清空Treeview
    for row in treeview.get_children():
        treeview.delete(row)

def save_mysql():
    try:
        conn = pymysql.connect(host='localhost', port=3306, user='root', password='1314520', database='mydata')
        cursor = conn.cursor()
        print('連線成功')
        # 插入訂單資料到主表，獲取訂單編號
        cursor.execute("INSERT INTO orders (order_date) VALUES (NOW())")
        cursor.execute("SELECT o.order_id FROM orders o ORDER BY order_id DESC limit 1")
        order_id = cursor.fetchone()[0]
        
        # 插入餐點資料到子表
        for item, info in order_dict.items():
            cursor.execute(
                "INSERT INTO order_items (order_id , item_name , price , quantity, total) VALUES (%s, %s, %s, %s, %s)",
                (order_id, item, info['price'], info['quantity'], info['total'])
            )

        conn.commit()

        # 關閉連接
        cursor.close()
        conn.close()

        # 將order_id傳到定義的open_confirm_win()函式
        open_confirm_win(order_id)
    
    except Exception as e:
        print('資料庫連線失敗', e)

def open_confirm_win(order_id):
    confirm_win = tk.Toplevel(win)
    confirm_win.title("確認訂單")
    confirm_win.geometry("400x300")

    # 計算總金額
    total_cost = sum(info['total'] for info in order_dict.values())
    print(order_dict)

    # 顯示訂單編號和總金額
    lab = tk.Label(confirm_win, text=f"訂單成功!!!", font='Arial, 16').place(x=60, y=50)
    lab2 = tk.Label(confirm_win, text=f"訂單編號：{order_id}", font='Arial, 16').place(x=60, y=100)
    lab3 = tk.Label(confirm_win, text=f"總金額：{total_cost}元", font='Arial, 16').place(x=60, y=150)

    # 清空訂單字典
    order_dict.clear()
   
    #清空Treeview
    for row in treeview.get_children():
        treeview.delete(row)

    #清空總金額
    total_value.set('')  # 清空總金額顯示

win = tk.Tk()

win.minsize(width=800, height=700)
win.title("MY POS")

# 初始化Treeview
columns = ('餐點名稱', '單價', '數量', '單項總金額')
treeview = ttk.Treeview(win, columns=columns, show='headings')
treeview.heading('餐點名稱', text='餐點名稱')
treeview.column("餐點名稱", width=150)
treeview.heading('單價', text='單價')
treeview.column("單價", width=150)
treeview.heading('數量', text='數量')
treeview.column("數量", width=150)
treeview.heading('單項總金額', text='單項總金額')
treeview.column("單項總金額", width=150)
treeview.place(x=50, y=400)


# 1.吐司類
x1 = 30
y1 = 30
lab0 = tk.Label(win, text='吐司類', font=("Arial", 20)).place(x=x1, y=y1)

lab1 = tk.Label(win, text='火腿蛋吐司：55元', font=('Arial', 12)).place(x=x1, y=y1+40)
btn_1_1 = tk.Button(win, text="+", padx=3, command=lambda: add_item('火腿蛋吐司', 55)).place(x=x1+170, y=y1+40)
btn_1_0 = tk.Button(win, text="-", padx=3, command=lambda: remove_item('火腿蛋吐司', 55)).place(x=x1+200, y=y1+40)


lab2 = tk.Label(win, text='培根蛋吐司：55元', font=('Arial', 12)).place(x=x1, y=y1+70)
btn_2_1 = tk.Button(win, text="+", padx=3, command=lambda: add_item('培根蛋吐司', 55)).place(x=x1+170, y=y1+70)
btn_2_0 = tk.Button(win, text="-", padx=3, command=lambda: remove_item('培根蛋吐司', 55)).place(x=x1+200, y=y1+70)

lab3 = tk.Label(win, text='鮪魚蛋吐司：60元', font=('Arial', 12)).place(x=x1, y=y1+100)
btn_3_1 = tk.Button(win, text="+", padx=3, command=lambda: add_item('鮪魚蛋吐司', 60)).place(x=x1+170, y=y1+100)
btn_3_0 = tk.Button(win, text="-", padx=3, command=lambda: remove_item('鮪魚蛋吐司', 60)).place(x=x1+200, y=y1+100)

lab4 = tk.Label(win, text='豬肉蛋吐司：60元', font=('Arial', 12)).place(x=x1, y=y1+130)
btn_4_1 = tk.Button(win, text="+", padx=3, command=lambda: add_item('豬肉蛋吐司', 60)).place(x=x1+170, y=y1+130)
btn_4_0 = tk.Button(win, text="-", padx=3, command=lambda: remove_item('豬肉蛋吐司', 60)).place(x=x1+200, y=y1+130)

# 蛋餅類
x2=300
y2=30
lab0 = tk.Label(win, text='蛋餅類', font=('Arial', 20)).place(x=x2, y=y2)

lab1 = tk.Label(win, text='火腿蛋餅：40元', font=('Arial', 12)).place(x=x2, y=y2+40)
btn_1_1 = tk.Button(win, text="+", padx=3, command=lambda: add_item('火腿蛋餅', 40)).place(x=x2+170, y=y2+40)
btn_1_0 = tk.Button(win, text="-", padx=3, command=lambda: remove_item('火腿蛋餅', 40)).place(x=x2+200, y=y2+40)

lab2 = tk.Label(win, text='培根蛋餅：45元', font=('Arial', 12)).place(x=x2, y=y2+70)
btn_1_1 = tk.Button(win, text="+", padx=3, command=lambda: add_item('培根蛋餅', 45)).place(x=x2+170, y=y2+70)
btn_1_0 = tk.Button(win, text="-", padx=3, command=lambda: remove_item('培根蛋餅', 45)).place(x=x2+200, y=y2+70)

lab3 = tk.Label(win, text='鮪魚蛋餅：45元', font=('Arial', 12)).place(x=x2, y=y2+100)
btn_1_1 = tk.Button(win, text="+", padx=3, command=lambda: add_item('鮪魚蛋餅', 45)).place(x=x2+170, y=y2+100)
btn_1_0 = tk.Button(win, text="-", padx=3, command=lambda: remove_item('鮪魚蛋餅', 45)).place(x=x2+200, y=y2+100)

lab4 = tk.Label(win, text='玉米蛋餅：30元', font=('Arial', 12)).place(x=x2, y=y2+130)
btn_1_1 = tk.Button(win, text="+", padx=3, command=lambda: add_item('玉米蛋餅', 30)).place(x=x2+170, y=y2+130)
btn_1_0 = tk.Button(win, text="-", padx=3, command=lambda: remove_item('玉米蛋餅', 30)).place(x=x2+200, y=y2+130)


# 其他餐點
x3=30
y3=220
lab0 = tk.Label(win, text='其他餐點', font=('Arial', 20)).place(x=x3, y=y3)

lab1 = tk.Label(win, text='鐵板麵：60元', font=('Arial', 12)).place(x=x3, y=y3+40)
btn_1_1 = tk.Button(win, text="+", padx=3, command=lambda: add_item('鐵板麵', 30)).place(x=x3+170, y=y3+40)
btn_1_0 = tk.Button(win, text="-", padx=3, command=lambda: remove_item('鐵板麵', 30)).place(x=x3+200, y=y3+40)

lab2 = tk.Label(win, text='泡菜炒麵：65元', font=('Arial', 12)).place(x=x3, y=y3+70)
btn_2_1 = tk.Button(win, text="+", padx=3, command=lambda: add_item('泡菜炒麵', 30)).place(x=x3+170, y=y3+70)
btn_2_0 = tk.Button(win, text="-", padx=3, command=lambda: remove_item('泡菜炒麵', 30)).place(x=x3+200, y=y3+70)

lab3 = tk.Label(win, text='蘿蔔糕：30元', font=('Arial', 12)).place(x=x3, y=y3+100)
btn_3_1 = tk.Button(win, text="+", padx=3, command=lambda: add_item('蘿蔔糕', 30)).place(x=x3+170, y=y3+100)
btn_3_0 = tk.Button(win, text="-", padx=3, command=lambda: remove_item('蘿蔔糕', 30)).place(x=x3+200, y=y3+100)

lab4 = tk.Label(win, text='荷包蛋：15元', font=('Arial', 12)).place(x=x3, y=y3+130)
btn_4_1 = tk.Button(win, text="+", padx=3, command=lambda: add_item('荷包蛋', 15)).place(x=x3+170, y=y3+130)
btn_4_0 = tk.Button(win, text="-", padx=3, command=lambda: remove_item('荷包蛋', 15)).place(x=x3+200, y=y3+130)

# 飲料
x4=300
y4=220
lab0 = tk.Label(win, text='飲料', font=('Arial', 20)).place(x=x4, y=y4)

lab1 = tk.Label(win, text='紅茶：20元', font=('Arial', 12)).place(x=x4, y=y4+40)
btn_1_1 = tk.Button(win, text="+", padx=3, command=lambda: add_item('紅茶', 20)).place(x=x4+170, y=y4+40)
btn_1_0 = tk.Button(win, text="-", padx=3, command=lambda: remove_item('紅茶', 20)).place(x=x4+200, y=y4+40)

lab2 = tk.Label(win, text='奶茶：20元', font=('Arial', 12)).place(x=x4, y=y4+70)
btn_1_1 = tk.Button(win, text="+", padx=3, command=lambda: add_item('奶茶', 20)).place(x=x4+170, y=y4+70)
btn_1_0 = tk.Button(win, text="-", padx=3, command=lambda: remove_item('奶茶', 20)).place(x=x4+200, y=y4+70)

lab3 = tk.Label(win, text='豆漿：20元', font=('Arial', 12)).place(x=x4, y=y4+100)
btn_1_1 = tk.Button(win, text="+", padx=3, command=lambda: add_item('豆漿', 20)).place(x=x4+170, y=y4+100)
btn_1_0 = tk.Button(win, text="-", padx=3, command=lambda: remove_item('豆漿', 20)).place(x=x4+200, y=y4+100)

lab4 = tk.Label(win, text='美式咖啡：35元', font=('Arial', 12)).place(x=x4, y=y4+130)
btn_1_1 = tk.Button(win, text="+", padx=3, command=lambda: add_item('美式咖啡', 35)).place(x=x4+170, y=y4+130)
btn_1_0 = tk.Button(win, text="-", padx=3, command=lambda: remove_item('美式咖啡', 35)).place(x=x4+200, y=y4+130)


# 計算總金額按鈕
confirm_button = tk.Button(win, text="總金額", font='Arial, 16', command=total)
confirm_button.place(x=70, y=640)
total_value = StringVar()  # 創建一個 StringVar 變數，用於儲存標籤的文字
label4 = tk.Label(win, textvariable=total_value, font='Arial, 16').place(x=170, y=645) 

# 計算總金額按鈕
clear_button = tk.Button(win, text="清除全部", font='Arial, 16', command=clear_list)
clear_button.place(x=270, y=640)

# 確認按鈕
confirm_button = tk.Button(win, text="確認", font='Arial, 16', command=save_mysql)
confirm_button.place(x=470, y=640)

win.mainloop()