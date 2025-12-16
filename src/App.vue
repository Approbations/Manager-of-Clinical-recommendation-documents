<script>
import DocListUnAuth from "./components/DocListUnAuth.vue";
import DocList from "./components/DocList.vue";
import DocListAdmin from "./components/DocListAdmin.vue";
import CreateDoc from "./components/CreateDoc.vue";
import SignUp from "./components/SignUp.vue";
import SignIn from "./components/SignIn.vue";
import LeaderBoard from "./components/LeaderBoard.vue";

export default {
  name: "App",
  components: {
    DocListUnAuth,
    DocList,
    DocListAdmin,
    CreateDoc,
    SignUp,
    SignIn,
    LeaderBoard,
  },
  data() {
    return {
      defurl: "//localhost:8002",
      activeComp: "SignIn",
      token_type: "",
      access_token: "",
      role: "",
      login: "",
    };
  },
  methods: {
    signOut() {
      this.role = this.type_access_token = "";
      this.activeComp = "SignIn";
    },
    auth(type, at, role, login) {
      this.token_type = type;
      this.access_token = at;
      this.role = role;
      this.login = login;
      this.admin("DocList");
    },
    admin(comp) {
      console.log(this.role);
      this.activeComp = this.role === "admin" ? comp + "Admin" : comp;
    },
  },
};
</script>

<template>
  <div v-if="role">
    <div id="btnbox">
      <button type="button" @click="activeComp = 'LeaderBoard'">
        Пользователи
      </button>
      <button type="button" @click="admin('DocList')">Список документов</button>
      <button type="button" @click="activeComp = 'CreateDoc'">
        Добавить документ
      </button>
      <button type="button" @click="signOut">Выйти из аккаунта</button>
    </div>
    <component
      :is="activeComp"
      :du="defurl"
      :role="role"
      :token_type="token_type"
      :access_token="access_token"
      :login="login"
    ></component>
  </div>
  <div v-else>
    <div id="btnbox">
      <button type="button" @click="activeComp = 'LeaderBoard'">
        Пользователи
      </button>
      <button type="button" @click="activeComp = 'DocListUnAuth'">
        Список документов
      </button>
      <button type="button" @click="activeComp = 'SignIn'">Войти</button>
      <button type="button" @click="activeComp = 'SignUp'">Регистрация</button>
    </div>
    <component
      v-if="activeComp === 'SignIn'"
      :is="activeComp"
      :du="defurl"
      @auth="auth"
    ></component>
    <component v-else :is="activeComp" :du="defurl"></component>
  </div>
</template>
