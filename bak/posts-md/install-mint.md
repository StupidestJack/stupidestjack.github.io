書接[上回](https://stupidestjack.github.io/blog/posts/linux-for-beginner.html)，
我提到了我會以Mint當作主要發行版。
所以，我們今天來裝Mint吧！

 > 提示：我使用的是Meee圖床，圖片方面在國內會有更好的瀏覽體驗。

## Part 1：下載Mint
我們直接到[Linux Mint官網](https://linuxmint.com/)，
應該可以看到下圖的畫面：
<img src="https://i.meee.com.tw/06nsQct.png" /><br>

點擊「Download」會進入到選擇版本的畫面：
<img src="https://i.meee.com.tw/BZaVlrD.png"><br>

通常會有Cinnamon、Xfce以及MATE（沒截到圖）三個版本。
這裡建議選擇最為華麗的Cinnamon版本。
點擊Cinnamon Edition下方的Download，
會進入到下載畫面。
<img src="https://i.meee.com.tw/oHDiGiw.png"><br>

如果你想使用BT下載，可以點擊BitTorrent Download旁的64-bit下載種子檔案。
往下滑則可以找到一般下載的站點。
Linux Mint的下載站點遍布世界各地，
比如台灣、日本、香港、法國等。
找到離自己最近的站點，並點擊機構名稱就會開始下載：
<img src="https://i.meee.com.tw/KRrL04X.png"><br>

下載速度依照網路速度，從三分鐘到一小時不等。

## Part 2：安裝和設定VirtualBox
有了 Linux Mint 的安裝光碟檔（ISO檔）之後，
我們可以先在虛擬機器內試試看。
虛擬機器類似於在電腦內建造一台虛擬的軟體電腦，
與一般的電腦功能幾乎相同。
以下我會教大家如何安裝VirtualBox虛擬機器軟體。
 > 提示1：如果你想直接在實體電腦上安裝，
 > 並且知道自己電腦的BIOS使用方式，請跳過這一步。
 > 實體電腦上安裝時，建議先關閉安全啟動。
 > 對於這方面，請搜尋你的電腦廠商或詢問AI。

 > 提示2：VirtualBox對新手以及Windows較為友好，
 > 但由於筆者電腦環境以Linux與(C槽空間見底的)Windows為主，
 > 後續安裝Linux Mint的演示會使用QEMU。
 > 不過安裝Linux Mint的階段用哪種虛擬機器都一樣。

進入到[VirtualBox官網](https://www.virtualbox.org/)之後，不要理會別的東西，
直接點Download即可。
<img src="https://i.meee.com.tw/3AostE0.png"><br>

進入下載畫面之後，在左邊的Platform Packages選擇自己的作業系統。
我這裡會以Windows演示。點擊Windows hosts就會下載Windows版安裝程式。
<img src="https://i.meee.com.tw/ZA4nDZP.png"><br>

 > 提示：因為筆者的Windows是英文，所以截圖也是英文的。
 > 我會做翻譯，不影響觀感；但翻的不對請在下面的留言板或是Email讓我知道！

打開安裝程式之後，點下一步。
<img src="https://i.meee.com.tw/4nCvhJJ.png"><br>

同意使用合約，然後再下一步。
<img src="https://i.meee.com.tw/0B8xsml.png"><br>

詢問要安裝的項目，預設全選再下一步。
<img src="https://i.meee.com.tw/y7UYSIX.png"><br>

這裡提示會暫時斷網，不過根據我的測試並不會，可以放心下一步。
<img src="https://i.meee.com.tw/nqP0Ahd.png"><br>

提示依賴項目不用理它，我從來沒遇過需要用到這些功能的時候。繼續下一步。
<img src="https://i.meee.com.tw/AcMPChI.png"><br>

給了三個選項：
 - 新增到開始選單
 - 建立桌面捷徑
 - 更改.ova及.ovf的文件開啟方式
按照個人喜好調整，看不懂就預設，然後下一步。
<img src="https://i.meee.com.tw/jR239f0.png"><br>

準備安裝，直接繼續！
<img src="https://i.meee.com.tw/1mychmn.png"><br>

安裝過程會在半分鐘到五分鐘不等，你可以休息一下。
<img src="https://i.meee.com.tw/FNfJLPD.png"><br>

安裝結束後點完成，就會自動開啟VirtualBox主畫面。
<img src="https://i.meee.com.tw/JjMwiXL.png"><br> 
<img src="https://i.meee.com.tw/GCN2wvU.png"><br>

選擇「基本模式」，然後按上方的「新增」，就會顯示建立虛擬機器的畫面。
<img src="https://i.meee.com.tw/6QtwE8u.png"><br>

輸入自己想要的名稱，如果指名Linux Mint，VirtualBox會自己辨識。
沒有也沒關係，把OS改成Linux，OS發行版改成Ubuntu，OS版本改成Ubuntu (64-bit)就可以了。
<img src="https://i.meee.com.tw/a8QLuL8.png"><br>

點擊「ISO映像」旁的向下箭頭，然後選「其他」。
找到剛剛下載的Linux Mint安裝光碟檔。
<img src="https://i.meee.com.tw/8pUnDj4.png"><br>

請把「以無人值守安裝繼續」取消，自己動手才好玩，而且又不難。 <!--我沒說謊，Mint真的不難啊-->
<img src="https://i.meee.com.tw/gyDDTfo.png"><br>

接著會建立虛擬機器的虛擬硬體。
基礎記憶體可以調大，但不能到紅色範圍；CPU數量也是；磁碟大小不能超過C槽的剩餘容量，但也不要剛好比較好。
<img src="https://i.meee.com.tw/EdRFuaH.png"><br>

最後會進入這個畫面，直接點完成即可。
<img src="https://i.meee.com.tw/Epmy0eF.png"><br>

看到這個畫面就代表虛擬機器建立成功了！點「啟動」就可以開機虛擬機器。
<img src="https://i.meee.com.tw/lzfUcxo.png"><br>

## Part 3：正式安裝Linux Mint！
相信我，非常簡單。

看到這個畫面之後，可以直接按Enter，或者等它。
實體機的樣子可能不一樣，但沒關係，一樣Enter。
<img src="https://i.meee.com.tw/QWZlbE0.png"><br>

然後就...進入桌面了？
莫慌！這是Live環境，相當於把整個系統塞進記憶體。
在裡面不論做什麼，重啟後都不會保留 ||是個看片的好地方|| 
<img src="https://i.meee.com.tw/VeHouJJ.png"><br>
