import tkinter as tk
import tkinter.messagebox
import random


class Game:
    """
    游戏主体\n
    请直接调用 main()
    :param level: 游戏难度默认0.5
    """

    def __init__(self, level=0.5):
        """
        初始化
        :param level: 游戏难度默认0.5
        """
        # 背景板数据
        self.board = {}
        # 难度等级
        self.level = level
        # system_make
        self.system_make = None
        # row
        self.row = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']

    def gui(self):
        """
        程序 gui
        """
        # 创建九宫格
        for i in range(11):
            for j in range(11):
                # 9个格之间画横线分开区域
                if i == 3 or i == 7:
                    label = tk.Label(root, width=2, font=("Arial", 1))
                    label.grid(row=i, column=j)
                    continue
                if j == 3 or j == 7:
                    label = tk.Label(root, width=2, font=("Arial", 1))
                    label.grid(row=i, column=j)
                    continue
                # 通过随机数判断是否显示填入空格
                if self.level >= random.random():
                    entry = tk.Entry(root, width=2, font=("Arial", 20))
                    entry.grid(row=i, column=j)
                    # 绑定回调函数到填入 Entry
                    entry.bind('<Return>', self.handler_adaptor(self.on_entry_change, i=i, j=j))
                else:
                    # 创建提示空格
                    entry = tk.Entry(root, width=2, font=("Arial", 20))
                    entry.grid(row=i, column=j)
                    # 根据行列位置确定与system_make生成的值位置
                    if j >= 8:
                        column = j - 2
                    elif j >= 4:
                        column = j - 1
                    else:
                        column = j
                    if i >= 8:
                        row = i - 2
                    elif i >= 4:
                        row = i - 1
                    else:
                        row = i
                    # 取 value
                    value = self.system_make[row][column]
                    # value在布局中的坐标位置
                    position = self.row[row] + str(column)
                    # 添加数值
                    self.board.update({
                        position: value
                    })
                    entry.insert(0, value)
                    entry.config(state="readonly")
        # 创建一个横栏把底部按钮和九宫格分开
        for i in range(11):
            label = tk.Label(root, width=2, font=("Arial", 1))
            label.grid(row=11, column=i)
        # 创建底部按钮
        # 确认按钮
        button = tk.Button(root, text="", command=self.click_event, width=2, height=1, bg="red")
        button.grid(row=12, column=5)

    def handler_adaptor(self, fun, **kwds):
        """
        中间传递函数，传递参数到绑定函数
        :param fun: 绑定按键函数
        :param kwds: 传入的参数   example：row = xx
        :return: 可传参函数
        """
        return lambda event, fun=fun, kwds=kwds: fun(event, **kwds)

    def on_entry_change(self, event, i, j):
        """
        entry框根据输入值情况改变存储值
        :param event: entry事件
        :param i: value所在行
        :param j: value所在列
        """
        # 获取当前的 Entry 对象
        entry = event.widget
        # 获取当前的文本值
        value = entry.get()
        if j >= 8:
            column = j - 2
        elif j >= 4:
            column = j - 1
        else:
            column = j
        if i >= 8:
            row = i - 2
        elif i >= 4:
            row = i - 1
        else:
            row = i
        # value在布局中的坐标位置
        position = self.row[row] + str(column)
        # 判断是否在字典里
        if position in self.board.keys():
            # 有就更新值
            self.board[position] = value
        else:
            # 没有就存一个新的
            self.board.update({
                position: value
            })

    def click_event(self):
        """确认按钮事件"""
        for index in range(9):
            try:
                val = [
                    int(tuple(sorted(self.board.items()))[_ + index * 9][1]) for _ in range(9)
                ]
            except IndexError:
                tk.messagebox.showinfo(title="答案填错啦", message="请你重新检查")
                return None
            if val != self.system_make[index]:
                tk.messagebox.showinfo(title="答案填错啦", message="请你重新检查")
                return None
        tk.messagebox.showinfo(title="太棒啦", message="都填对了")

    def generate_sudoku(self) -> list[list[int]]:
        """
        自动生成一组九宫格数据
        :return: 生成的数据，多维数组
        """
        # 创建一个 9x9 的二维列表
        sudoku = [[0 for _ in range(9)] for _ in range(9)]
        # 填充对角线上的 3 个 3x3 子方阵
        for j in range(3):
            nums = list(range(1, 10))
            random.shuffle(nums)
            for k in range(3):
                sudoku[j * 3 + k][j * 3:(j + 1) * 3] = nums[k * 3:k * 3 + 3]
        # 对已填充的子方阵进行回溯搜索
        val = self.backtrack(sudoku, 0, 3)
        if not val:
            return self.generate_sudoku()
        return sudoku

    def backtrack(self, sudoku: list, row: int, col: int, ) -> bool:
        """
        回溯算法
        :param sudoku: 生成的数据
        :param row: 行
        :param col: 列
        :return:  是否正确
        """
        if col == 9:
            row += 1
            col = 0
            if row == 9:
                return True

        # 如果当前位置已经有数字了，就跳过
        if sudoku[row][col] != 0:
            return self.backtrack(sudoku, row, col + 1)

        # 枚举当前位置可以填的数字
        nums = list(range(1, 10))
        random.shuffle(nums)
        for num in nums:
            if self.is_valid(sudoku, row, col, num):
                sudoku[row][col] = num
                if self.backtrack(sudoku, row, col + 1):
                    return True
                sudoku[row][col] = 0

        return False

    def is_valid(self, sudoku: list, row: int, col: int, num: int) -> bool:
        """
        生成的数据是否正确
        :param sudoku: 生成的数据
        :param row: 行
        :param col: 列
        :param num: 数字
        :return:  是否正确
        """
        # 检查行和列是否含有重复数字
        for i in range(9):
            if sudoku[row][i] == num or sudoku[i][col] == num:
                return False

        # 检查所在的 3x3 子方阵是否含有重复数字
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                if sudoku[i][j] == num:
                    return False

        return True

    def main(self):
        """
        主运行函数
        """
        # 先生成数据
        self.system_make = self.generate_sudoku()
        # for i in self.system_make:
        #     print(i)
        # print("-----------")
        self.gui()


if __name__ == '__main__':
    # 创建tk主体
    root = tk.Tk()
    root.title("数独")
    # 创建游戏主体
    Game().main()
    # 运行
    root.mainloop()
