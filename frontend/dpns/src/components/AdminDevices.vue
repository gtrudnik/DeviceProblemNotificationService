<template>
  <div class="container col-md-6">
        <h2 class="text-center mb-3 mx-auto">Ваши устройства</h2>
        <div class="mx-auto" v-for="device in devices" :key="device.id">
            <router-link :to="`/device/${device.id}`" style="color: inherit; text-decoration: none;">
                <div class="card mb-4">
                  <div class="card-body">
                    <h5 class="card-title">{{ device.name }}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">{{ device.location }}</h6>
                    <p class="card-text" v-show="device.type"><strong>Тип устройства:</strong> {{ device.type }}</p>
                    <p class="card-text" v-show="device.description"><strong>Описание:</strong> {{ device.description }}</p>
                  </div>
                </div>
            </router-link>
        </div>
        <div class="d-flex justify-content-center mb-5">
            <router-link to="/create_device" class="w-100 btn btn-primary text-white">Добавить устройство</router-link>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'admin_devices',
  data() {
    return {
      devices: [],
    };
  },
  async created() {
    axios.defaults.withCredentials = true;
    try {
      const response = await axios.get(`${this.$urlServer}/devices/get_by_admin`,);
      const devicesData = response.data;
      console.log(devicesData);
      const devices = [];
      for (const device of devicesData) {
        const device_ = {
          id: device.id,
          name: device.name,
          location: `корпус ${device.building}, этаж ${device.floor}`,
          type: device.type_device,
          description: device.description,
        }
        if (device.room){
            device_.location += `, аудитория ${device.room}`
        }
        if (device.location_description){
            device_.location += `, ${device.location_description}`
        }
        devices.push(device_);
      }
      this.devices = devices;
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
