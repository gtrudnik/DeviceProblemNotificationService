<template>
  <div class="container mt-5">
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
              </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'create_problem',
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
      const response = await axios.get(`http://127.0.0.1:8000/problems/get_by_author`,);
      const problemsData = response.data;
      const problems = [];
      for (const problem of problemsData) {
        const problem_ = {
          id: problem.id,
          deviceName: problem.device,
          deviceLocation: 'Кабинет 101',
          problemType: problem.type_problem,
          problemDescription: problem.description,
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
