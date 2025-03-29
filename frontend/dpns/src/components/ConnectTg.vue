<template>
    <div class="container mt-5" v-if="is_visible_form">
        <h2 class="mb-4">Подключение аккаунта к телеграм</h2>
        <form @submit.prevent="connect_tg">
            <div class="form-group">
                <label for="telegram-id">Telegram ID (числовое значение)</label>
                <input v-model="tg_id" type="number" class="form-control" id="telegram-id" placeholder="Введите Telegram ID" required>
            </div>
            <div class="form-group">
                <label for="code">Код (6-значное число)</label>
                <input v-model="tg_code" type="number" maxlength="6" class="form-control" id="code" placeholder="Введите 6-значный код" required>
            </div>
            <button type="submit" class="btn btn-primary">Подключить</button>
        </form>
    </div>
    <div class="container mt-5" v-if="is_visible_tg_label">
        <h2 class="mb-4">Ваш аккаунт подключён к телеграм</h2>
        <p>Id вашего телеграм: {{ tg_id_label }} </p>
        <button @click="unconnect_tg" type="submit" class="btn btn-primary">Отключить телеграм</button>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'connectTg',
  data() {
    return {
      is_visible_form: false,
      is_visible_tg_label: false,
      tg_id_label: '',
      tg_id: '',
      tg_code: ''
    };
  },
  watch: {
    tg_id_label(newValue) {
      console.log(newValue)
      if (this.tg_id_label) {
        this.is_visible_form = false;
        this.is_visible_tg_label = true;
      } else {
        this.is_visible_form = true;
        this.is_visible_tg_label = false;
      }
    },
  },
  async created() {
    axios.defaults.withCredentials = true;
    try {
      const response = await axios.post(`${this.$urlServer}/auth/get_tg`,);
      console.log(response.data);
      this.tg_id_label = response.data.tg_id;
    } catch (error) {
      if (error.response.status === 401) {
        localStorage.removeItem('role')
        console.error('Доступ запрещен. Пожалуйста, войдите в систему.');
        this.$router.push('/auth_form');
      }
      console.error(error.response.data);
    }
    await this.show_label();
  },
  methods: {
    async connect_tg() {
        try {
          const params = new URLSearchParams({
            tg_id: this.tg_id,
            tg_code: this.tg_code,
          });
          const response = await axios.post(`${this.$urlServer}/auth/connect_tg?${params.toString()}`,);
          console.log(response.data);
          this.tg_id_label = this.tg_id;
          this.tg_id = '';
          this.tg_code = '';
        } catch (error) {
          if (error.response.status === 401) {
            localStorage.removeItem('role')
            console.error('Доступ запрещен. Пожалуйста, войдите в систему.');
            this.$router.push('/auth_form');
          }
          console.error(error.response.data);
        }
    },
    async unconnect_tg() {
        try {
          const response = await axios.post(`${this.$urlServer}/auth/unconnect_tg`,);
          console.log(response.data);
          this.tg_id_label = '';
        } catch (error) {
          if (error.response.status === 401) {
            localStorage.removeItem('role')
            console.error('Доступ запрещен. Пожалуйста, войдите в систему.');
            this.$router.push('/auth_form');
          }
          console.error(error.response.data);
        }
    },
    async show_label() {
      if (this.tg_id_label) {
        this.is_visible_form = false;
        this.is_visible_tg_label = true;
      } else {
        this.is_visible_form = true;
        this.is_visible_tg_label = false;
      }
    }
  },
};
</script>

<style scoped>
</style>