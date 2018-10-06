

### Level 2

(1) Where the vulnerable source code locates:
We can input some text in the text box and then the text will be shown in the post list.

![L2_input](/Users/zhangyingzhe/Downloads/L2_input.png)

First we try to directly input the `<script>alert("Hello World")</script>` in the text box. Then the new post is shown but the `alert` not. So we go into the source code and I find the following sentence.

![L2_code](/Users/zhangyingzhe/Downloads/L2_code.png)

`post[i].message` is the text of our input and it will be added to the `html`. Finally, the `html` will be added to `containerEl.innerHTML`.  If the `script` is dynamically embedded by `innerHTML`, the browser will treat it as normal text and will not maintain it as a `script` node in the `DOM`. So it cannot be found when called.



(2) How to trigger vulnerability:

There is an easy way. Since the data is stored on the server side. We can use the `onerror` event, and the function that handles the error will be called. In this way, we can put the `alert` into the function. For instance, we can write a post like this:

 `<img src="cannot_find_img.png" onerror=alert("Yingzhe")>`. 

The server cannot find the image so there will be an error and the `onerror` function will be called. Then we can see the `alert`.

![L2_alert](/Users/zhangyingzhe/Downloads/L2_alert.png)



### Level 4

(1) Where the vulnerable source code locates:

We can input a number to the timer and then the timer start. At the same time we can see the number is added to the parameters in the URL.

![](/Users/zhangyingzhe/Downloads/L4_input.png)

![](/Users/zhangyingzhe/Downloads/L4_param.png)

Let's go into the source code. On the python side, our input will be saved in the `timer` and then the `timer.html` will be rendered using the `timer`.

![L4_pythonside](/Users/zhangyingzhe/Downloads/L4_pythonside.png)

And in the `timer.html`, the `startTimer()` function will be called when the page is loading. As we can see, `'{{ timer }}'` is the parameter and we can treat that as a string.

![L4_timerfunc](/Users/zhangyingzhe/Downloads/L4_timerfunc.png)



(2) How to trigger vulnerability:

Since we can treat the ` timer` parameter as a string, we can include`')` in our input to end the `startTimer()` first and then add the `alert` . Then whole input looks like this: 

`3');alert('Yingzhe`.

When the page loading, the following will be called. `startTimer(3); alert('Yingzhe');`. So we can see the `alert`. 

![L4_alert](/Users/zhangyingzhe/Downloads/L4_alert.png)



### Level 6

(1) Where the vulnerable source code locates:

We can change the string after `#` in the URL. If we change that to `www.google.com`, we can see the result in the page.

![L6_URL](/Users/zhangyingzhe/Downloads/L6_URL.png)

So it looks like the page will load the URL. Let's take a look at the source code.

![](/Users/zhangyingzhe/Downloads/L6_sourcecode.png)

The function will create a `<script>` element and put the content of the URL into the `<script>`. 

(2) How to trigger vulnerability:

Actually we can write the `alert()` into a JavaScript file but there is a easy way: use the **Data URLs**

**Data URLs**

> URLs prefixed with the `data:` scheme, allow content creators to embed small files inline in documents.
>
> ```
> data:[<mediatype>][;base64],<data>
> ```

So we can input the URL like this:

`https://xss-game.appspot.com/level6/frame#data:text/plain,alert("Yingzhe")`

`<mediatype>` is `text/plain` and `<data>` is `alert("Yingzhe")`.

So we can see the alert.

![L6_alert](/Users/zhangyingzhe/Downloads/L6_alert.png)









