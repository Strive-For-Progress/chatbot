建議做以下動作前先自行備份pair資料夾

我將靖文新的機器人部分重新嵌入，把資料夾裡的東西下載完丟入\pair\ccu_ai_lab_backend\即可，  
前端\pair\ccu_ai_lab_frontend\依舊維持不變，  
我是選擇綜合秉廷跟我原先的想法，看回傳的值是甚麼再決定要不要Call其他的函式或的新的response  
![image](https://user-images.githubusercontent.com/82814921/208320335-6b8bb981-8e54-446e-9257-5594129edea5.png)  
  
為此在靖文的code弄了一個專屬網站呼叫的case2函式  
![image](https://user-images.githubusercontent.com/82814921/208320306-3365ba5f-2aaf-4da4-8455-7f4704852f60.png)  
保證回傳的值永遠都會是字串,讓其他前後端盡量維持不變  
