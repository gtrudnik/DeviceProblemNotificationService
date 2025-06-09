<template>
  <div class="container">
        <h2 class="text-center mb-3 mx-auto">Ваши заявки о проблемах на устройстве</h2>
        <div class="mb-3 text-center">
            <div class="btn-group" role="group" aria-label="Кнопки фильтрации">
                <button :class="{'btn-primary': activeFilter === 'all', 'btn-secondary': activeFilter !== 'all'}" @click="setFilter('all')"
                    type="button" class="btn" id="all">Все</button>
                <button :class="{'btn-primary': activeFilter === 'active', 'btn-secondary': activeFilter !== 'active'}" @click="setFilter('active')"
                    type="button" class="btn" id="active">Активные</button>
                <button :class="{'btn-primary': activeFilter === 'completed', 'btn-secondary': activeFilter !== 'completed'}" @click="setFilter('completed')"
                    type="button" class="btn" id="completed">Завершенные</button>
            </div>
        </div>
         <div class="col-md-9 mx-auto" v-for="problem in problems_displayed" :key="problem.id">
            <div class="card mb-4">
              <div class="card-body">
                <h5 class="card-title">{{ problem.deviceName }}</h5>
                <h6 class="card-subtitle mb-2 text-muted">{{ problem.deviceLocation }}</h6>
                <p class="card-text" v-show="problem.problemType"><strong>Тип проблемы:</strong> {{ problem.problemType }}</p>
                <p class="card-text" v-show="problem.problemDescription"><strong>Описание:</strong> {{ problem.problemDescription }}</p>
                <p class="card-text"><strong>Статус:</strong> {{ problem.status }}</p>
                <p class="card-text"><strong>Дата создания заявки:</strong> {{ problem.date_create }}</p>
                <div v-show="problem.status === 'Решено'">
                    <details v-show="!problem.grade">
                      <summary>Оставить отзыв</summary>
                      <form>
                      <label>Оценка</label>
                      <br>
                        <div class="form-check form-check-inline">
                          <input class="form-check-input" v-model="selectedValue" type="radio" name="inlineRadioOptions" id="inlineRadio1" value="1">
                          <label class="form-check-label" for="inlineRadio1">1</label>
                        </div>
                        <div class="form-check form-check-inline">
                          <input class="form-check-input" v-model="selectedValue" type="radio" name="inlineRadioOptions" id="inlineRadio2" value="2">
                          <label class="form-check-label" for="inlineRadio2">2</label>
                        </div>
                        <div class="form-check form-check-inline">
                          <input class="form-check-input" v-model="selectedValue" type="radio" name="inlineRadioOptions" id="inlineRadio3" value="3">
                          <label class="form-check-label" for="inlineRadio1">3</label>
                        </div>
                        <div class="form-check form-check-inline">
                          <input class="form-check-input" v-model="selectedValue" type="radio" name="inlineRadioOptions" id="inlineRadio4" value="4">
                          <label class="form-check-label" for="inlineRadio2">4</label>
                        </div>
                        <div class="form-check form-check-inline">
                          <input class="form-check-input" v-model="selectedValue" type="radio" name="inlineRadioOptions" id="inlineRadio5" value="5">
                          <label class="form-check-label" for="inlineRadio2">5</label>
                        </div>
                      <div class="form-group">
                        <label for="feedback_text">Описание проблемы</label>
                        <textarea v-model="feedback_text" class="form-control" id="problemDescription" rows="4" placeholder="Опишите вашу проблему здесь..."></textarea>
                      </div>
                      <button class="btn btn-primary mt-2" @click="send_feedback(problem.id, selectedValue, feedback_text)">Отправить</button>
                      </form>
                    </details>
                    <details v-show="problem.grade">
                      <summary>Отзыв</summary>
                      <label>Оценка: {{ problem.grade }}</label>
                      <br>
                      <label>Комментарий: {{ problem.feedback }}</label>
                    </details>
                </div>
              </div>
            </div>
        </div>
    </div>
</template>

<script>
import { format } from 'date-fns';
import axios from 'axios';

export default {
  name: 'user_problem',
  data() {
    return {
    activeFilter: 'all',
    problems_displayed: [],
    problems: [],
    };
  },
  async created() {
    axios.defaults.withCredentials = true;
    try {
      const response = await axios.get(`${this.$urlServer}/problems/get_by_author`,);
      const problemsData = response.data;
      const problems = [];
      problemsData.sort((a, b) => new Date(b.date_created) - new Date(a.date_created));
      for (const problem of problemsData) {
        const problem_ = {
          id: problem.id,
          deviceName: problem.device_name,
          deviceLocation: `корпус ${problem.device_building}, этаж ${problem.device_floor}, аудитория ${problem.device_room}`,
          problemType: problem.type_problem,
          problemDescription: problem.description,
          date_create: format(problem.date_created, 'dd.MM.yyyy HH:mm'),
          grade: problem.grade,
          feedback: problem.feedback,
        }

        if (problem.resolver){
            if (problem.status === "resolved"){
                problem_.status = "Решено"
            } else {
                problem_.status = "В работе"
            }
        } else{
            problem_.status = "В ожидании"
        }
        problems.push(problem_);
      }
      this.problems = problems;
      this.fill_problems();
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
    setFilter(filter) {
      this.activeFilter = filter;
      console.log(this.activeFilter);
      this.fill_problems();
    },
    fill_problems() {
      const problems_displayed = [];
      for (const problem of this.problems) {
        if (this.activeFilter == "all"){
            problems_displayed.push(problem);
        }
        if (this.activeFilter == "completed" && problem.status === "Решено"){
            problems_displayed.push(problem);
        }
        if (this.activeFilter == "active" && problem.status !== "Решено"){
            problems_displayed.push(problem);
        }
        this.problems_displayed = problems_displayed;
      }
    },
    async send_feedback(problem_id, grade, feedback) {
      console.log(problem_id);
      if (grade) {
        console.log(grade);
        try {
          const params = new URLSearchParams({
            problem_id: problem_id,
            grade: grade,
          });
          if (feedback) {
            params.append('comment', feedback);
          }
          const response = await axios.post(`${this.$urlServer}/problems/feedback?${params.toString()}`,);
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
      console.log(feedback);
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
