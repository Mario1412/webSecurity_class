

##Exploit the Vulnerability

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

Since regular expressions are case-sensitive, we can also type that `http` as `HTtp` to bypass the check. Or type a space`' '` before the `http`.



## Patching

### Level 2

First we create a server using python flask. It will send the CSP header to the client(in next step of the home work) and render the html. In the JavaScript side, we add a encodeText() function to encode the input as the plain text.

![patching_levle2_1](/Users/zhangyingzhe/Downloads/patching_level2_1.png)

The logic is creating a `<div> ` and putting the text in its `innerText` (for Firefox is `textContent`). And then we extract the `innerHTML` of the `div` as the plain text.  Before we put the input of the user to the html, we encode the `post[].message` as plain text. The page finally displays the original text typed by the user. 

![patching_level2_2](/Users/zhangyingzhe/Downloads/patching_level2_2.png)

Cause the first post is a *Welcome Message* , we will skip it and then encode the following post. In this case, the result will be

![patching_level2_3](/Users/zhangyingzhe/Downloads/patching_level2_3.png)



### Level 4

This time we will check the user's input on the sever side. We create a `check_timer()` function to get the submission value of the timer and check if it is a number using `isdigit()`. The sever will return the right page only when the user input a valid value.

![patching_level4_1](/Users/zhangyingzhe/Downloads/patching_level4_1.png)

On the client side, the only change is that we add the `check_timer` as a `GET` mothed to the action in the `<form>` element. The client will send the request including the timer value to the sever.

![patching_level4_2](/Users/zhangyingzhe/Downloads/patching_level4_2.png)

In this case, if the input is not a number, the sever will return a error page to the client.

![patching_level4_3](/Users/zhangyingzhe/Downloads/patching_level4_3.png)

When we download the source code and run it locally, we find if we put the JavaScript code in the`<head>` the selector cannot find the element with its id because the page has not finished loading. So we put the code of selector in the `<body>`. And in the next CSP step, we put that in a JS file. 

![patching_level4_4](/Users/zhangyingzhe/Downloads/patching_level4_4.png)



### Level 6

Due to the protocol limitation, the content behind the `#` of the URL cannot be included in the request, so we cannot check the input in the address bar on the server side. So the main problem is to modify the regular expression part.

When we get the content after `#`, we will delete all the space `' '` in that using Regex.

![patching_level6_1](/Users/zhangyingzhe/Downloads/patching_level6_1.png)

Double backslash symbol `//` is another way to use `https` or `http`, so the next step is check wether the content starting with `//`.

![patching_level6_2](/Users/zhangyingzhe/Downloads/patching_level6_2.png)

After that, get the first 8 character of the content as the `urlHead` and transfer that to lowercase. In these way, we can check if the url uses HTTP, data url, FTP, SMTP and other protocols. Once it is detected that it uses the above protocol, an error message will be displayed.

![patching_level6_3](/Users/zhangyingzhe/Downloads/patching_level6_3.png)

The result is as follows,

![patching_level6_4](/Users/zhangyingzhe/Downloads/patching_level6_4.png)