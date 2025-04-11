<template>
  <div class="container col-md-7">
        <h2 class="text-center mb-3 mx-auto">Типы проблем</h2>
        <h5 class="mb-3">Тип устройства: {{ device_type }}</h5>
        <div class="mx-auto" v-for="device_type_problem in device_type_problems" :key="device_type_problem.id">
            <div class="card mb-2">
              <div class="card-body">
                <h5 class="card-title">{{ device_type_problem.name_problem }}</h5>
                <p class="card-text" v-show="device_type_problem.description">Описание: {{ device_type_problem.description }}</p>
              </div>
            </div>
        </div>
        <h5 class="text-center mt-4">Добавить новый тип проблемы</h5>

        <form class="mb-5">
            <div class="form-group">
                <label for="problemType">Название типа проблемы</label>
                <input type="text" class="form-control" v-model="newDeviceProblemType" placeholder="Введите название типа проблемы" required>
            </div>

            <div class="form-group">
                <label for="problemDescription">Описание типа проблемы</label>
                <textarea v-model="problemTypeDescription" class="form-control" rows="4" placeholder="Опишите вашу проблему здесь..."></textarea>
            </div>

            <button @click="addDeviceTypeProblem" type="submit" class="btn btn-primary">Добавить</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'device_type_problems',
  data() {
    return {
      device_type_problems: [],
      device_type: '',
      newDeviceProblemType: '',
      problemTypeDescription: '',
      device_type_id: this.$route.params.id,
    };
  },
  async created() {
    axios.defaults.withCredentials = true;
    try {
      const response = await axios.get(`${this.$urlServer}/devices/get_type_device?type_device_id=${this.device_type_id}`,);
      this.device_type = response.data.type_device
    } catch (error) {
      if (error.response.status === 401) {
        localStorage.removeItem('role')
        this.$router.push('/auth_form');
      }
      console.error(error.response.data);
    }

    try {
      const response = await axios.get(`${this.$urlServer}/problems/get_types?type_device=${this.device_type_id}`,);
      const devicesTypeProblemsData = response.data;
      console.log(devicesTypeProblemsData);
      this.device_type_problems = devicesTypeProblemsData;
    } catch (error) {
      if (error.response.status === 401) {
        localStorage.removeItem('role')
        this.$router.push('/auth_form');
      }
      console.error(error.response.data);
    }
  },
  methods: {
    async addDeviceTypeProblem(){
        event.preventDefault();
        try {
          const params = new URLSearchParams({
            name: this.newDeviceProblemType,
            type_device_id: this.device_type_id,
          });
          if (this.problemTypeDescription !== "") {
            params.append('description', this.problemTypeDescription);
          }
          const response = await axios.post(`${this.$urlServer}/problems/create_problem_type?${params.toString()}`,);
          console.log(response.data);
          this.newDeviceProblemType = '';
          this.problemTypeDescription = '';
        } catch (error) {
          if (error.response.status === 401) {
            localStorage.removeItem('role')
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
