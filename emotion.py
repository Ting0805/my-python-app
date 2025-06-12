import tkinter as tk
from tkinter import messagebox
import csv
import os

class EmotionSurveyApp:
    def __init__(self, root, word_list):
        self.root = root
        self.word_list = word_list
        self.current_word_index = 0
        self.results = []
        
        # 设置窗口标题和大小
        self.root.title("词汇情感判断调查")
        self.root.geometry("500x400")
        self.root.configure(bg='#f0f0f0')  # 调试用背景色
        
        # 初始化所有组件
        self.create_widgets()
        
        # 显示第一个词
        self.show_next_word()
    
    def create_widgets(self):
        """创建并初始化所有界面组件"""
        # 显示当前词汇（加大字体和边距）
        self.word_label = tk.Label(self.root, text="", 
                                 font=('Microsoft YaHei', 24),
                                 bg='#f0f0f0')
        self.word_label.pack(pady=30, fill=tk.X)
        
        # 情感选择按钮框架（添加背景色便于调试）
        self.emotion_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.emotion_frame.pack(pady=15)
        
        # 情感选择按钮
        self.emotion_var = tk.StringVar()
        emotions = [("积极", "positive"), ("中性", "neutral"), ("消极", "negative")]
        for text, emotion in emotions:
            btn = tk.Radiobutton(self.emotion_frame, text=text, 
                                variable=self.emotion_var, value=emotion,
                                font=('Microsoft YaHei', 14), bg='#f0f0f0')
            btn.pack(side=tk.LEFT, padx=15)
        
        # 下一步按钮（更醒目的样式）
        self.next_btn = tk.Button(self.root, text="下一步 →", 
                                command=self.show_intensity_page,
                                font=('Microsoft YaHei', 14),
                                state=tk.DISABLED,
                                bg='#4CAF50', fg='white')
        self.next_btn.pack(pady=20)
        
        # 绑定情感选择变化事件
        self.emotion_var.trace("w", self.enable_next_button)
        
        # 预创建程度选择页面组件（但不显示）
        self.create_intensity_page()
    
    def create_intensity_page(self):
        """预先创建程度选择页面组件"""
        self.intensity_frame = tk.Frame(self.root, bg='#f0f0f0')
        
        tk.Label(self.intensity_frame, text="请选择情感程度(1-5):", 
                font=('Microsoft YaHei', 16), bg='#f0f0f0').pack(pady=10)
        
        self.intensity_var = tk.IntVar()
        intensity_frame = tk.Frame(self.intensity_frame, bg='#f0f0f0')
        intensity_frame.pack()
        for i in range(1, 6):
            btn = tk.Radiobutton(intensity_frame, text=str(i), 
                               variable=self.intensity_var, value=i,
                               font=('Microsoft YaHei', 14), bg='#f0f0f0')
            btn.pack(side=tk.LEFT, padx=10)
        
        self.confirm_btn = tk.Button(self.root, text="确认", 
                                   command=self.record_and_continue,
                                   font=('Microsoft YaHei', 14),
                                   bg='#2196F3', fg='white')
        
        self.back_btn = tk.Button(self.root, text="← 返回", 
                                command=self.back_to_emotion_page,
                                font=('Microsoft YaHei', 14))
    
    def enable_next_button(self, *args):
        """当选择情感后启用下一步按钮"""
        self.next_btn.config(state=tk.NORMAL if self.emotion_var.get() else tk.DISABLED)
    
    def show_next_word(self):
        """显示下一个词汇"""
        if self.current_word_index < len(self.word_list):
            current_word = self.word_list[self.current_word_index]
            self.word_label.config(text=current_word)
            self.emotion_var.set("")  # 重置选择
            self.next_btn.config(state=tk.DISABLED)
        else:
            self.save_results()
            messagebox.showinfo("完成", "调查已完成！感谢参与。")
            self.root.quit()
    
    def show_intensity_page(self):
        """显示程度选择页面"""
        # 隐藏当前页面元素
        self.word_label.pack_forget()
        self.emotion_frame.pack_forget()
        self.next_btn.pack_forget()
        
        # 显示程度选择页面
        self.intensity_frame.pack(pady=40)
        self.confirm_btn.pack(pady=15)
        self.back_btn.pack(pady=5)
        self.intensity_var.set(0)  # 重置选择
    
    def back_to_emotion_page(self):
        """返回到情感选择页面"""
        self.intensity_frame.pack_forget()
        self.confirm_btn.pack_forget()
        self.back_btn.pack_forget()
        
        self.word_label.pack(pady=30)
        self.emotion_frame.pack(pady=15)
        self.next_btn.pack(pady=20)
    
    def record_and_continue(self):
        """记录结果并继续下一个词"""
        if not self.intensity_var.get():
            messagebox.showerror("错误", "请选择情感程度")
            return
        
        self.results.append({
            "word": self.word_list[self.current_word_index],
            "emotion": self.emotion_var.get(),
            "intensity": self.intensity_var.get()
        })
        
        self.current_word_index += 1
        self.back_to_emotion_page()
        self.show_next_word()
    
    def save_results(self):
        """保存结果到CSV文件"""
        os.makedirs("results", exist_ok=True)
        filename = "results/survey_results.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["word", "emotion", "intensity"])
            writer.writeheader()
            writer.writerows(self.results)
        messagebox.showinfo("保存成功", f"结果已保存到 {filename}")

# 测试词汇列表
word_list = [
    "白痴", "疯子", "过分", "光荣", "热烈", "技巧", "变态", "停止", "恶劣", "透明", "获胜", "欢呼", "白痴", "通知", "一致", "规矩", "混蛋", "欢喜", "热情", "愤怒", "烦躁", "人性", "闪耀", "活泼", "垃圾", "词汇", "暴力", "中奖", "通知", "说明", "实际", "恶劣", "道理", "怒火", "冠军", "复仇", "透露", "凯旋", "光荣", "气死", "亲吻", "欢呼", "罪恶", "灿烂", "破坏", "思考", "积极", "热情", "欢呼", "可恶", "感激", "混蛋", "罪恶", "重生", "清理", "诅咒", "美满", "讨厌", "专门", "公开", "毁灭", "喜庆", "管理", "愤怒", "破坏", "亲吻", "想象", "专门", "垃圾", "凯旋", "专门", "讨厌", "透明", "热闹", "人性", "想象", "道理", "光荣", "约定", "公开", "自动", "贱人", "感激", "贱人", "灿烂", "直觉", "自动", "训练", "说明", "愚蠢", "精彩", "烦躁", "思考", "怒火", "气死", "管理", "道理", "闪耀", "可恶", "通知", "固定", "热爱", "恶心", "喜庆", "说明", "报复", "规矩", "诅咒", "透露", "侮辱", "固定", "过分", "摧毁", "疯子", "热爱", "积极", "滚蛋", "发觉", "想象", "凌辱", "奇迹", "精彩", "最佳", "一致", "助手", "亲吻", "不满", "滚蛋", "获胜", "公开", "暴力", "闪亮", "罪恶", "固定", "逻辑", "垃圾", "毁灭", "停止", "奇迹", "约定", "诅咒", "欢乐", "摧毁", "重生", "美满", "感激", "冠军", "战胜", "欢喜", "恶心", "美满", "发觉", "愚蠢", "热烈", "白痴", "热爱", "技巧", "暴力", "变态", "不满", "欢笑", "冷静", "清理", "中奖", "清晰", "侮辱", "喜庆", "关怀", "闪耀", "助手", "直觉", "关怀", "财产", "管理", "愤怒", "战胜", "复仇", "财产", "自动", "最佳", "兴奋", "人性", "冠军", "讨厌", "思考", "报复", "训练", "变态", "灿烂", "一致", "怒火", "欢乐", "透明", "疯子", "逻辑", "侮辱", "抗议", "直觉", "清晰", "技巧", "复仇", "规矩", "约定", "冷静", "愚蠢", "战胜", "兴奋", "狂欢", "过分", "实际", "发觉", "中奖", "抗议", "实际", "承认", "放屁", "闪亮", "不满", "停止", "凌辱", "欢笑", "烦躁", "滚蛋", "财产", "清理", "助手", "闪亮", "承认", "活泼", "积极", "兴奋", "逻辑", "最佳", "热闹", "遵守", "奇迹", "摧毁", "热情","透露", "抗议", "贱人", "欢笑", "恶劣", "热闹", "可恶", "恶心", "热烈", "冷静", "狂欢", "重生", "关怀", "凯旋", "遵守", "精彩", "放屁", "遵守", "欢喜", "凌辱", "混蛋", "气死", "清晰", "报复", "承认", "狂欢", "放屁", "获胜", "破坏", "毁灭", "欢乐", "训练", "活泼"
]

if __name__ == "__main__":
    root = tk.Tk()
    app = EmotionSurveyApp(root, word_list)
    root.mainloop()