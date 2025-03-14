<template>
  <div class="container mt-5">
        <h2 class="text-center">Заявка о проблеме на устройстве</h2>
        <p>Название устройства: {{ device_name }} </p>
        <p>Тип: {{ device_type }}</p>
        <p>Расположение: {{ device_location }}</p>
        <p>Описание: {{ device_description }}</p>
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
  data() {
    return {
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
    try {
      const response = await axios.get('http://127.0.0.1:8000/devices/get?device_id=2');
      const deviceData = response.data;
      this.device_name = deviceData.name; // подставьте нужные поля из API
      this.device_type = deviceData.type_device; // замените на реальный ключ из вашего ответа
      this.device_location = `корпус ${deviceData.building}, этаж ${deviceData.floor}, аудитория ${deviceData.room}`; // замените на реальный ключ из вашего ответа
      this.device_description = deviceData.description; // замените на реальный ключ из вашего ответа
      this.device_type_id = deviceData.type_device_id;
      console.log(deviceData);
    } catch (error) {
      console.error(error.response.data); // Обработайте ошибку
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
      console.log(problem_types);
    } catch (error) {
      console.error(error.response.data); // Обработайте ошибку
    }
  },
  methods: {
    async sendProblem() {
        event.preventDefault();
        try {
          console.log(this.problemDescription);
          console.log(1);
          const params = new URLSearchParams({
            device_id: 2,
          });
          if (this.problemDescription !== "") {
            params.append('description', this.problemDescription);
          }
          if (this.problemType !== "Другая проблема") {
            params.append('type_problem', this.problemType);
          }
          console.log(`http://127.0.0.1:8000/problems/create?${params.toString()}`);
          const response = await axios.post(`http://127.0.0.1:8000/problems/create?${params.toString()}`);
          console.log(response);


        } catch (error) {
          console.error(error.response.data); // Обработайте ошибку
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
