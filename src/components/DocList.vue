<script>
export default {
  name: "DocList",
  props: {
    // Переданные компоненту значения
    du: {
      type: String,
      required: true,
    },
    role: String,
    token_type: {
      type: String,
      required: true,
    },
    access_token: {
      type: String,
      required: true,
    },
    login: {
      type: String,
      required: true,
    },
  },
  data: function () {
    // Переменные компонента
    return {
      dList: [],
      inp: null,
      Page: 1,
      maxP: 1,
      mydocs: false,
    };
  },
  created: function () {
    this.getpage();
  },
  methods: {
    del(ind) {
      const id = this.dList[ind].id_cr;
      fetch(this.du + "/mydoclist/" + id, {
        method: "DELETE",
        headers: {
          Authorization: this.token_type + " " + this.access_token,
        },
      });
      this.dList.splice(ind, 1);
    },
    refr() {
      if (this.mydocs) {
        this.get_my_docs();
      } else {
        this.getpage();
      }
    },
    prev() {
      --this.Page;
      this.refr();
    },
    next() {
      ++this.Page;
      this.refr();
    },
    async getpage() {
      const url =
        this.du +
        "/doclist/paginated?size=30&page=" +
        (this.Page - 1).toString();
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
    async opdoc(id) {
      try {
        const response = await fetch(this.du + "/doclist/" + id);
        if (!response.ok) {
          throw new Error(`Response status: ${response.status}`);
        }
      } catch (error) {
        console.error(error.message);
      }
    },
    async searchDoc() {
      if (this.inp) {
        this.dList = [];
        const url = this.mydocs
          ? this.du + "/get_my_docs?size=100&page="
          : this.du + "/doclist/paginated?size=100&page=";
        try {
          for (this.Page = 0; this.Page < this.maxP; ++this.Page) {
            const response = this.mydocs
              ? await fetch(url + this.Page.toString(), {
                  headers: {
                    Authorization: this.token_type + " " + this.access_token,
                  },
                })
              : await fetch(url + this.Page.toString());
            if (!response.ok) {
              throw new Error(`Response status: ${response.status}`);
            }
            const data = await response.json();
            this.maxP = data.total_pages;
            data.items.forEach((element) => {
              if (
                element.id_cr.includes(this.inp) ||
                element.title.includes(this.inp)
              ) {
                this.dList.push(element);
              }
            });
          }
          this.Page = 0;
        } catch (error) {
          console.error(error.message);
        }
      } else {
        this.Page = 1;
        this.refr();
      }
    },
    switchmodes() {
      this.mydocs = !this.mydocs;
      this.Page = 1;
      this.refr();
      this.inp = "";
    },
    async get_my_docs() {
      const url =
        this.du + "/get_my_docs?size=30&page=" + (this.Page - 1).toString();
      try {
        const response = await fetch(url, {
          headers: {
            Authorization: this.token_type + " " + this.access_token,
          },
        });
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
  },
};
</script>

<template>
  <textarea
    id="search"
    placeholder="Введите название документа"
    v-model="inp"
  ></textarea>
  <button id="srch-btn" type="button" @click="searchDoc">
    <svg view-box="0 0 25 25" stroke="black" stroke-width="1px">
      <circle cx="11" cy="10" r="10" fill="none"></circle>
      <path d="M18.07,17.07L25,25"></path>
    </svg>
  </button>
  <button v-if="mydocs" type="button" @click="switchmodes">
    Все документы
  </button>
  <button v-else type="button" @click="switchmodes">Мои документы</button>
  <ul class="feed" id="doc-feed">
    <li v-for="(value, ind) in dList" :key="value.id_cr">
      <button id="open-btn" @click="opdoc(value.id_cr)">
        {{ value.id_cr }} | {{ value.title }}
      </button>
      <button
        v-if="login === value.creator"
        id="del-btn"
        type="button"
        @click="del(ind)"
      >
        Удалить
      </button>
    </li>
  </ul>
  <div id="pg-box" v-if="Page">
    <button type="button" @click="prev" v-if="Page > 1">Предыдущая</button>
    <p>{{ Page }}</p>
    <button type="button" @click="next" v-if="Page < maxP">Следующая</button>
  </div>
</template>
