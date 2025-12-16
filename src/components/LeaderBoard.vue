<script>
export default {
  name: "LeaderBoard",
  props: {
    // Переданные компоненту значения
    du: {
      type: String,
      required: true,
    },
    role: String,
    token_type: String,
    access_token: String,
    login: String,
  },
  data: function () {
    // Переменные компонента
    return {
      dList: [],
      Page: 1,
      maxP: 1,
      chlogin: "",
      chfname: "",
      chlname: "",
      chrole: "",
      chcrat: "",
      chdocnt: undefined,
      redact: false,
    };
  },
  created: function () {
    this.getpage();
    if (this.login) {
      this.opprof(this.login);
    }
  },
  methods: {
    prev() {
      --this.Page;
      this.getpage();
    },
    next() {
      ++this.Page;
      this.getpage();
    },
    async getpage() {
      const url =
        this.du + "/profiles?size=30&page=" + (this.Page - 1).toString();
      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`Response status: ${response.status}`);
        }
        const data = await response.json();
        this.dList = data.items;
        this.maxP = data.total_pages;
      } catch (error) {
        console.error(error.message);
      }
    },
    async opprof(login) {
      try {
        const response = await fetch(this.du + "/profile?login=" + login);
        if (!response.ok) {
          throw new Error(`Response status: ${response.status}`);
        }
        const data = await response.json();
        const usr = data[0];
        this.chlogin = usr.login;
        this.chfname = usr.first_name;
        this.chlname = usr.last_name;
        this.chrole = usr.role;
        this.chcrat = usr.created_at;
        this.chdocnt = usr.documents_count;
      } catch (error) {
        console.error(error.message);
      }
    },
    toredact() {
      this.redact = true;
      if (this.role === "client") {
        this.chfname = this.chlname = "";
      } else {
        this.chlogin = this.chrole = this.chcrat = "";
        this.chfname = this.chlname = "su-norm";
      }
    },
    outredact() {
      this.redact = false;
      this.opprof(this.login);
    },
    async change() {
      try {
        const response = await fetch(this.du + "/profile", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: this.token_type + " " + this.access_token,
          },
          body: JSON.stringify({
            first_name: this.chfname,
            last_name: this.chlname,
          }),
        });
        if (!response.ok) {
          throw new Error(`Response status: ${response.status}`);
        }
        this.outredact();
      } catch (error) {
        console.error(error.message);
      }
    },
    async addadmin() {
      this.chfname = this.chlname = "su-norm";
      if (this.chlogin && this.chrole) {
        const response = await fetch(this.du + "/registry", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            login: this.chlogin,
            password: this.chrole,
            role: "admin",
          }),
        });
        if (response.ok) {
          const data = await response.json();
          this.chcrat = data.message;
          this.chlogin = this.chrole = "";
          this.getpage();
        } else {
          this.chcrat = `Response status: ${response.status}`;
        }
      } else {
        this.chcrat = "";
        if (!this.chlogin) {
          this.chfname = "su-req";
          this.chcrat = "Отсутствует логин. ";
        }
        if (!this.chrole) {
          this.chlname = "su-req";
          this.chcrat += "Отсутствует пароль.";
        }
      }
    },
  },
};
</script>

<template>
  <ul class="feed" id="prof-feed">
    <li v-for="value in dList" :key="value.login">
      <button id="open-btn" @click="opprof(value.login)">
        {{ value.documents_count }} | {{ value.login }}
      </button>
    </li>
  </ul>
  <div id="pg-box" v-if="Page">
    <button type="button" @click="prev" v-if="Page > 1">Предыдущая</button>
    <p>{{ Page }}</p>
    <button type="button" @click="next" v-if="Page < maxP">Следующая</button>
  </div>
  <div v-if="chlogin && !redact">
    <div id="prof-box">
      <p>Логин: {{ chlogin }}</p>
      <p>Имя: {{ chfname }}</p>
      <p>Фамилия: {{ chlname }}</p>
      <div v-if="chlogin === login">
        <button type="button" @click="toredact" v-if="role === 'client'">
          Редактировать
        </button>
        <button type="button" @click="toredact" v-else>Добавить админа</button>
      </div>
    </div>
    <div id="prof-box">
      <p>Роль: {{ chrole }}</p>
      <p>Дата создания: {{ chcrat }}</p>
      <p>Количество документов: {{ chdocnt }}</p>
    </div>
  </div>
  <div v-else-if="redact">
    <div v-if="role === 'client'">
      <label for="lb-fname">Имя</label>

      <br />
      <input
        type="text"
        id="lb-fname"
        v-model="chfname"
        placeholder="Введите имя"
      /><br />
      <label for="lb-lname">Фамилия</label>

      <br />
      <input
        type="text"
        id="lb-lname"
        v-model="chlname"
        placeholder="Введите фамилию"
      />
      <button type="button" @click="change">Сохранить</button>
      <button type="button" @click="outredact">Отмена</button>
    </div>
    <div v-else>
      <label for="lb-login">Логин<span style="color: red">*</span></label>
      <br />
      <input
        type="text"
        id="lb-login"
        :class="chfname"
        v-model="chlogin"
        placeholder="Введите логин"
      /><br />
      <label for="lb-password">Пароль<span style="color: red">*</span></label>
      <br />
      <input
        type="password"
        id="lb-password"
        :class="chlname"
        v-model="chrole"
        placeholder="Введите пароль"
      />

      <button type="button" @click="addadmin">Добавить</button>
      <button type="button" @click="outredact">Отмена</button>
      <p>{{ chcrat }}</p>
    </div>
  </div>
</template>
