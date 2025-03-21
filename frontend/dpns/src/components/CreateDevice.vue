<template>
  <div class="container mt-5 mb-5">
        <h2 class="text-center">Создание нового устройства</h2>
        <form >
            <div class="form-row">
                <label for="deviceName">Название устройства</label>
                <input type="text" class="form-control" id="deviceName" v-model="deviceName" placeholder="Введите название устройства" required>
            </div>
            <div class="form-group">
                <label for="problemType">Тип устройства</label>
                <select class="form-control" id="problemType" v-model="problemType">
                    <option v-for="(i, index) in problemTypes" :key="index" :value="i">{{ i }}</option>
                </select>
            </div>
            <div class="form-group">
                <label for="deviceDescription">Описание устройства</label>
                <textarea class="form-control" id="deviceDescription" v-model="deviceDescription" rows="3" placeholder="Введите описание устройства" required></textarea>
            </div>
            <div class="form-group">
                <label for="building">Здание</label>
                <input type="text" class="form-control" id="building" v-model="building" placeholder="Введите название здания" required>
            </div>
            <div class="form-group">
                <label for="floor">Этаж</label>
                <input type="number" min="-10" step="1" class="form-control" id="floor"
                v-model="floor" placeholder="Введите этаж" required>
            </div>
            <div class="form-group">
                <label for="office">Кабинет</label>
                <input type="text" class="form-control" id="room" v-model="room" placeholder="Введите номер кабинета" required>
            </div>
            <div class="form-group">
                <label for="locationDescription">Описание локации</label>
                <textarea class="form-control" id="locationDescription" v-model="locationDescription" rows="3" placeholder="Введите описание локации" required></textarea>
            </div>
            <button @click="createDevice" type="submit" class="btn btn-primary">Создать</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'create_device',
  data() {
    return {
      deviceName: '',
      deviceDescription: '',
      building: '',
      floor: 1,
      room: '',
      locationDescription: '',

      problemType: 'Другой тип',
      problemTypes: ['Другой тип'],
    };
  },
  async created() {
    axios.defaults.withCredentials = true;
    try {
      const response = await axios.get(`http://127.0.0.1:8000/devices/get_all_type_devices`);
      const problemTypesData = response.data;
      console.log(problemTypesData);
      const problem_types = ['Другой тип'];
      for (const problemType of problemTypesData) {
        problem_types.push(problemType.type_device);
        console.log(problemType.type_device);
      }
      this.problemTypes = problem_types;
    } catch (error) {
      console.error(error.response.data);
    }
  },
  methods: {
    async createDevice() {
        event.preventDefault();
        try {
          const params = new URLSearchParams({
            name: this.deviceName,
            description: this.deviceDescription,
            building: this.building,
            floor: this.floor,
            room: this.room,
            location_description: this.locationDescription
          });
          if (this.problemType !== "Другой тип") {
            params.append('type_device', this.problemType);
          }
          const response = await axios.post(`http://127.0.0.1:8000/devices/create?${params.toString()}`,);
          console.log(response.data);
          this.$router.push('user_problems');
        } catch (error) {
          console.error(error.response.data);
        }
    },
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
