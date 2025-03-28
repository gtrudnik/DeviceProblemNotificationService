<template>
    <div class="container mt-5">
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
</template>

<script>
import axios from 'axios';

export default {
  name: 'connectTg',
  data() {
    return {
      tg_id: '',
      tg_code: ''
    };
  },
  methods: {
    async connect_tg() {
        try {
          const params = new URLSearchParams({
            tg_id: this.tg_id,
            tg_code: this.tg_code,
          });
          console.log(1);
          const response = await axios.post(`${this.$urlServer}/auth/connect_tg?${params.toString()}`,);
          console.log(2);
          console.log(response.data);
          console.log(3);
        } catch (error) {
          console.log(3);
          if (error.response.status === 401) {
            localStorage.removeItem('role')
            console.error('Доступ запрещен. Пожалуйста, войдите в систему.');
            this.$router.push('/auth_form');
          }
          console.error(error.response.data);
        }
    },
  },
};
</script>

<style scoped>
</style>