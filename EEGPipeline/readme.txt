原始数据中record开头的文件包含了所有的标签信息，一般是完整的，而下面提到的evt.bdf可能是缺少标签的。
标签对应的时间体现在evt.bdf文件中，可以使用文本编辑器直接打开。
如+1 +116.98000Trigger-Out:255  中间的+116.9800代表了标签对应的时间(s)。

1. extractNumberFromEvt.py代码可用于从上述的evt.bdf文件中仅提取时间信息。注意evt.bdf只需要保留和标签相关的行
2. findLabelLine.py可从record开头的文件中提取不同事件对应的下标。
3. filterFileByLine.py可结合第2步的事件的下标和第一步得到的时间信息的文件 最终得到某类事件对应的触发时间。
4. als_dataset.py最终通过第3步得到的不同事件label时间信息构造npy数据 用于后续的处理