<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Login</title>
  <!-- 引入 Vue.js -->
  <script src="https://cdn.jsdelivr.net/npm/vue@2.6.14/dist/vue.js"></script>
</head>
<body>
  <div id="app">
    <h2>Login</h2>
    <!-- 登录表单 -->
    <form @submit.prevent="login">
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username">
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password">
      </div>
      <button type="submit">Login</button>
    </form>
    <!-- 登录结果提示 -->
    <div v-if="message" style="margin-top: 10px; color: red;">{{ message }}</div>
  </div>

  <script>
    new Vue({
      el: '#app',
      data() {
        return {
          username: '',
          password: '',
          message: ''
        };
      },
      methods: {
        login() {
          // 这里可以添加登录逻辑，比如发送登录请求到后端
          // 模拟登录成功和失败的情况
          if (this.username === 'admin' && this.password === '123456') {
            this.message = 'Login successful!';
          } else {
            this.message = 'Invalid username or password!';
          }
        }
      }
    });
  </script>
</body>
</html>
