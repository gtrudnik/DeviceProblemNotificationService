<template>
  <div class="container">
        <h2 class="text-center mb-3 mx-auto">Пользователи сервиса</h2>
        <div class="col-md-9 mx-auto" v-for="user in users" :key="user.id">
            <div class="card mb-4">
              <div class="card-body">
                <h6 class="card-title" v-show="user.login">Логин: {{ user.login }}</h6>
                <h6 class="card-title" v-show="user.tg">Телеграм: {{ user.tg }}</h6>

                <div class="form-group d-flex align-items-center">
                    <label for="roleSelect-{{ user.id }}" class="mr-2 mb-0">Роль:</label>
                    <select v-model="user.role" class="form-control mr-2" id="roleSelect-{{ user.id }}">
                        <option value="banned">Banned</option>
                        <option value="user">User </option>
                        <option value="admin">Admin</option>
                        <option value="super_admin">Super Admin</option>
                    </select>
                    <button @click="updateRole(user.id, user.role)" class="btn btn-primary">Сохранить</button>
                </div>
              </div>
            </div>


        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'user_list',
  data() {
    return {
      users: [],
    };
  },
  async created() {
    axios.defaults.withCredentials = true;
    try {
      const response = await axios.get(`${this.$urlServer}/users/get_all`,);
      const usersData = response.data;
      console.log(usersData);
      const users = [];
      for (const user of usersData) {
        const user_ = {
          id: user.id,
          login: user.login,
          tg: user.tg_id,
          role: user.role,

        }
        users.push(user_);
      }
      this.users = users;
    } catch (error) {
      if (error.response.status === 401) {
        localStorage.removeItem('role')
        console.error('Доступ запрещен. Пожалуйста, войдите в систему.');
        this.$router.push('/auth_form');
      }
      console.error(error.response.data);
    }
  },
  methods: {
    async updateRole(user_id, role){
        event.preventDefault();
        try {
          const params = new URLSearchParams({
            new_role: role,
            user_id: user_id,
          });
          const response = await axios.post(`${this.$urlServer}/users/change_role?${params.toString()}`,);
          console.log(response.data);
        } catch (error) {
          if (error.response.status === 401) {
            localStorage.removeItem('role')
            console.error('Доступ запрещен. Пожалуйста, войдите в систему.');
            this.$router.push('/auth_form');
          }
          console.error(error.response.data);
        }
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
