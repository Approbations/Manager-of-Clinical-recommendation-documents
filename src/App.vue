<script>
import DocListUnAuth from "./components/DocListUnAuth.vue";
import DocList from "./components/DocList.vue";
import DocListAdmin from "./components/DocListAdmin.vue";
import CreateDoc from "./components/CreateDoc.vue";
import CreateDocAdmin from "./components/CreateDocAdmin.vue";
import SignUp from "./components/SignUp.vue";
import SignIn from "./components/SignIn.vue";

export default {
  name: "App",
  components: {
    DocListUnAuth,
    DocList,
    DocListAdmin,
    CreateDoc,
    CreateDocAdmin,
    SignUp,
    SignIn,
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
      this.activeComp = "DocList";
    },
    admin(comp) {
      this.activeComp = this.role === "admin" ? comp + "Admin" : comp;
    },
  },
};
//delete & createdoc (admin can add 'creator') are admin-only features.
//POST /get_my_docs & POST /createmydoc & DELETE /mydoclist/{id} are client feature
</script>

<template>
  <div v-if="role">
    <div id="btnbox">
      <button type="button" @click="admin('DocList')">Список документов</button>
      <button type="button" @click="admin('CreateDoc')">
        Добавить документ
      </button>
      <button type="button" @click="signOut">Выйти из аккаунта</button>
    </div>
    <component
      v-if="activeComp.includes('CreateDoc')"
      :is="activeComp"
      :du="defurl"
      :token_type="token_type"
      :access_token="access_token"
    ></component>
    <component
      v-else
      :is="activeComp"
      :du="defurl"
      :token_type="token_type"
      :access_token="access_token"
      :login="login"
    ></component>
  </div>
  <div v-else>
    <div id="btnbox">
      <button type="button" @click="activeComp = 'SignIn'">Войти</button>
      <button type="button" @click="activeComp = 'SignUp'">Регистрация</button>
      <button type="button" @click="activeComp = 'DocListUnAuth'">
        Список документов
      </button>
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
