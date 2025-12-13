<script>
export default {
  name: "SignIn",
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
  emits: ["auth"],
  methods: {
    async log_in() {
      if (this.login && this.password) {
        const response = await fetch(this.du + "/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            login: this.login,
            password: this.password,
          }),
        });
        this.lclass = this.pclass = "su-norm";
        if (response.ok) {
          const data = await response.json();
          this.$emit(
            "auth",
            data.token_type,
            data.access_token,
            data.user.role,
            data.user.login
          );
        } else {
          this.msg = Error(`Response status: ${response.status}`).message;
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
  <button type="button" @click="log_in">Войти</button>
  <p>{{ msg }}</p>
</template>
