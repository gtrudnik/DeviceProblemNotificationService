<template>
  <div class="container mt-5">
        <h2 class="text-center">Заявка о проблеме на устройстве</h2>
        <p>Название устройства: {{ device_name }} </p>
        <p v-show="device_type">Тип: {{ device_type }}</p>
        <p v-show="device_location">Расположение: {{ device_location }}</p>
        <p v-show="device_description">Описание: {{ device_description }}</p>
        <hr>
        <form>
            <div class="form-group">
                <label for="problemType">Тип проблемы</label>
                <select class="form-control" id="problemType" v-model="problemType">
                    <option v-for="(i, index) in problemTypes" :key="index" :value="i">{{ i }}</option>
                </select>
            </div>

            <div class="form-group">
                <label for="problemDescription">Описание проблемы</label>
                <textarea v-model="problemDescription" class="form-control" id="problemDescription" rows="4" placeholder="Опишите вашу проблему здесь..."></textarea>
            </div>

            <button @click="sendProblem" type="submit" class="btn btn-primary">Отправить</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'create_problem',
  data() {
    return {
      device_id: this.$route.params.id,
      device_name: '',
      device_type: '',
      device_location: '',
      device_description: '',

      problemType: 'Другая проблема',
      problemTypes: ['Другая проблема'],
      problemDescription: '',
      submitted: false
    };
  },
  async created() {
    console.log(this.$route.params.id);
    axios.defaults.withCredentials = true;
    try {
      const response = await axios.get(`http://127.0.0.1:8000/devices/get?device_id=${this.device_id}`,
      {
      //withCredentials: true,
      }
      );
      const deviceData = response.data;
      this.device_name = deviceData.name;
      this.device_type = deviceData.type_device;
      this.device_location = `корпус ${deviceData.building}, этаж ${deviceData.floor}, аудитория ${deviceData.room}`;
      this.device_description = deviceData.description;
      this.device_type_id = deviceData.type_device_id;
      console.log(deviceData);
    } catch (error) {
      console.error(error.response.data);
    }
    try {
      const response = await axios.get(`http://127.0.0.1:8000/problems/get_types?type_device=${this.device_type_id}`);
      const problemTypesData = response.data;
      const problem_types = ['Другая проблема'];
      for (const problemType of problemTypesData) {
        problem_types.push(problemType.name_problem);
        console.log(problemType.name_problem);
      }
      this.problemTypes = problem_types;
    } catch (error) {
      console.error(error.response.data);
    }
  },
  methods: {
    async sendProblem() {
        event.preventDefault();
        try {
          const params = new URLSearchParams({
            device_id: this.device_id,
          });
          if (this.problemDescription !== "") {
            params.append('description', this.problemDescription);
          }
          if (this.problemType !== "Другая проблема") {
            params.append('type_problem', this.problemType);
          }
          const response = await axios.post(`http://127.0.0.1:8000/problems/create?${params.toString()}`,);
          console.log(response.data);
          this.$router.push('/user_problems');
        } catch (error) {
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
