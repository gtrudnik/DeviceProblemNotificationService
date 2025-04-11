<template>
  <div class="container col-md-7">
        <h2 class="text-center mb-3 mx-auto">Типы устройств</h2>
        <div class="mx-auto" v-for="device in device_types" :key="device.id">
            <router-link :to="`/device_type_problems/${device.id}`" style="color: inherit; text-decoration: none;">
                <div class="card mb-2">
                    <div class="card-body">
                        <h5 class="mb-0">{{ device.type_device }}</h5>
                    </div>
                </div>
            </router-link>
        </div>
        <h5 class="text-center mt-4">Добавить новый тип устройства</h5>
        
        <form class="mb-5">
            <div class="form-group">
                <label for="problemType">Название типа проблемы</label>
                <input type="text" class="form-control" v-model="newDeviceType" placeholder="Введите название" required>
            </div>
            <button @click="addDeviceType" type="submit" class="btn btn-primary">Добавить</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'device_types',
  data() {
    return {
      device_types: [],
      newDeviceType: '',
    };
  },
  async created() {
    axios.defaults.withCredentials = true;
    try {
      const response = await axios.get(`${this.$urlServer}/devices/get_all_type_devices`,);
      const devicesTypesData = response.data;
      console.log(devicesTypesData);
      this.device_types = devicesTypesData;
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
    async addDeviceType(){
        event.preventDefault();
        try {
          const params = new URLSearchParams({
            name: this.newDeviceType,
          });
          const response = await axios.post(`${this.$urlServer}/devices/new_type?${params.toString()}`,);
          console.log(response.data);
          this.newDeviceType = '';
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
