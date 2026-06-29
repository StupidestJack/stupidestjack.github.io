不知不覺間，我也用了兩個月半的Arch Linux了。  
那剛好，我段考終於是考完了，就來寫一下使用心得吧。

## 什麼是Arch Linux？
~~世界上最棒的Linux發行版。~~  
我不會這麼說，哪個發行版好用因人而異。比如Linus Torvalds用的是Fedora，或者Wiwi官大為用的是Linux Mint等等。  
Arch Linux是一個從最小基本系統開始安裝的Linux發行版，你需要自行增加你需要的工具，從指令行（TTY界面）開始，疊加視窗管理器、桌面環境等工具。  
在維基百科，Arch被形容成適合「不懼怕命令列的中進階Linux使用者」，還挺貼切。  

## 配置
我在我的GIGABYTE G5 GE上安裝Arch。  
 - CPU: 12th Gen Intel(R) Core(TM) i5-12500H
 - RAM: DDR4 3200MHz 16GiB(8+8)
 - 硬碟: NVMe PCIe 4.0 512GB SSD
 - GPU: NVIDIA GeForce RTX 3050 Mobile 
 - 螢幕： 1920x1080 144Hz

## 安裝體驗
我也重灌過好幾次了。我最近重灌這一次改用了CachyOS核心，但系統仍然是原生Arch。  
安裝教學我就不放了，請在[Arch Wiki](https://wiki.archlinux.org/title/Main_page_)取得具體的教學 :P  
其實對我來講算簡單的，因為Arch Wiki寫的非常詳細，你可以根據自己的要求來修改。  
我使用過非常多桌面環境和視窗管理器，包含KDE Plasma、Sway、Hyprland、i3-wm、GNOME（幾乎沒怎麼用）、Cinnamon、Xfce...。  
搞了半天我最後選擇了KDE Plasma作為主力，保留Sway作為需要專注時使用。

## 使用體驗
無論如何，我以後應該就真的以Arch為主力，不會在主電腦上長期使用其他發行版了。  
首先，Arch Linux在安裝完成之後真的很有成就感，這個懂的都懂好不好。  
此外，Arch的原版倉庫只有開源的方案，連NVIDIA也改為使用`nvidia-open`系列驅動程式，這讓我用的非常舒服。  
而且我現在的工作流，不是不需要Wine，就是Wine不能跑，除了Proton（這個算嗎lol），這讓我不需要做太多思考，Pacman裡面幾乎都有我要的軟體；要是真的沒有，我還可以去AUR裡面翻。

## 另一個讓我難過的點
我們班上**都是文盲**。
不是我說啊，班上連作業系統都不知道的大概有一半以上，導致我只要在班上基本上沒同伴，不是自言自語就是找別的話題。
 > *「I wish everybody was as nice as I am.」* -- Linus Torvalds  
 > [這裡來的](https://youtu.be/Q4SWxWIOVBM?si=7TbdoAlGi4jmjLHl&t=76)  
 > ㄊㄇㄉ覺得自己在這放這句超不要臉

## Arch的缺點
對嘛，Arch當然不是完美的。  
首先，它是**滾動更新**發行版，這免不了上下游各種軟體衝突的問題。  
對於老玩家，這或許還好；對於新手，這可能無法獨自處理啊。

此外，Arch的純指令安裝（現在也有TUI的`archinstall`腳本）也非常麻煩。  
早上八點開始裝系統，最慢的時候我能裝到下午才進桌面（即使我有過18分鐘速通的狀況）。

***但沒關係，它仍然是我用過最適合我的Linux發行版。***
**So NVIDIA f||uc||k you**
