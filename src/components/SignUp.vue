<script>
export default {
  name: "SignUp",
  props: {
    du: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      login: "",
      password: "",
      lclass: "su-norm",
      pclass: "su-norm",
      msg: "",
    };
  },
  methods: {
    async register() {
      if (this.login && this.password) {
        this.lclass = this.pclass = "su-norm";
        const response = await fetch(this.du + "/registry", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            login: this.login,
            password: this.password,
          }),
        });
        if (response.ok) {
          const data = await response.json();
          this.msg = data.message;
          this.login = this.password = "";
        } else {
          this.msg = `Response status: ${response.status}`;
        }
      } else {
        this.msg = "";
        if (!this.login) {
          this.lclass = "su-req";
          this.msg = "Отсутствует логин. ";
        }
        if (!this.password) {
          this.pclass = "su-req";
          this.msg += "Отсутствует пароль.";
        }
      }
    },
  },
};
</script>

<template>
  <label for="su-login">Логин <span style="color: red">*</span></label>
  <br />
  <input
    type="text"
    id="su-login"
    :class="lclass"
    v-model="login"
    placeholder="Введите логин"
  /><br />
  <label for="su-password">Пароль <span style="color: red">*</span></label>
  <br />
  <input
    type="password"
    id="su-password"
    :class="pclass"
    v-model="password"
    placeholder="Введите пароль"
  /><br />
  <button type="button" @click="register">Зарегистрироваться</button>
  <p>{{ msg }}</p>
</template>
