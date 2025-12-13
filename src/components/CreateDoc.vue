<script>
export default {
  name: "CreateDoc",
  props: {
    du: {
      type: String,
      required: true,
    },
    token_type: {
      type: String,
      required: true,
    },
    access_token: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      iclass: "su-norm",
      tclass: "su-norm",
      msg: "",
    };
  },
  methods: {
    async createdoc() {
      //check if it sends when not filled required fields. Try adding popovers for clarity of what's happening.
      const form = document.getElementById("addDoc");
      const fD = new FormData(form);
      this.msg = "";
      this.iclass = this.tclass = "su-norm";
      if (fD.get("doc_id") && fD.get("title") && fD.get("file").size) {
        const response = await fetch(this.du + "/createmydoc", {
          method: "POST",
          headers: {
            Authorization: this.token_type + " " + this.access_token,
          },
          body: fD,
        });
        if (response.ok) {
          form.reset();
          this.msg = "Документ успешно добавлен.";
        } else {
          this.msg = `Response status: ${response.status}.`;
        }
      } else {
        if (!fD.get("doc_id")) {
          this.iclass = "su-req";
        }
        if (!fD.get("title")) {
          this.tclass = "su-req";
        }
        if (!fD.get("file").size) {
          this.msg = "Прикрепите файл.";
        }
      }
    },
  },
};
</script>
<template>
  <form id="addDoc">
    <label for="inp-id">ID <span style="color: red">*</span></label>
    <br />
    <input type="text" name="doc_id" id="inp-id" :class="iclass" /><br />
    <label for="inp-title"
      >Наименование <span style="color: red">*</span></label
    >
    <br />
    <input type="text" name="title" id="inp-title" :class="tclass" /><br />
    <label for="inp-mcb">МКБ-10</label><br />
    <input type="text" name="mcb" id="inp-mcb" /><br />
    <label for="inp-acat">Возрастная группа</label><br />
    <input type="text" name="age_category" id="inp-acat" /><br />
    <label for="inp-dev">Разработчик</label><br />
    <input type="text" name="developer" id="inp-dev" /><br />
    <label for="inp-file">Документ <span style="color: red">*</span></label>
    <br />
    <input type="file" name="file" id="inp-file" accept=".pdf" /><br />
    <button type="button" @click="createdoc">Добавить</button>
  </form>
  <p>{{ msg }}</p>
</template>
