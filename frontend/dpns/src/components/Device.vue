<template>
  <div class="container mb-5">
        <h2 class="text-center">Информация об устройстве</h2>
        <form>
            <div class="form-group">
                <label for="deviceName">Название устройства: {{ device_name }}</label>
            </div>
            <div class="form-group">
                <label for="deviceType">Тип устройства: {{ device_type }}</label>
            </div>
            <div class="form-group">
                <label for="device_description">Описание устройства</label>
                <textarea class="form-control" id="device_description" v-model="device_description" rows="3" placeholder="Введите описание устройства" required></textarea>
            </div>

            <div class="form-row">
                <div class="form-group col-md-4">
                    <label for="building">Здание</label>
                    <input type="text" class="form-control" id="building" v-model="building" placeholder="Введите название здания" required>
                </div>
                <div class="form-group col-md-4">
                    <label for="floor">Этаж</label>
                    <input type="number" min="-10" step="1" class="form-control" id="floor" v-model="floor" placeholder="Введите этаж" required>
                </div>
                <div class="form-group col-md-4">
                    <label for="room">Кабинет</label>
                    <input type="text" class="form-control" id="room" v-model="room" placeholder="Введите номер кабинета" required>
                </div>
            </div>

            <div class="form-group">
                <label for="location_description">Описание локации</label>
                <textarea class="form-control" id="location_description" v-model="location_description" rows="3" placeholder="Введите описание локации" required></textarea>
            </div>
            <button @click="updateDevice" type="submit" class="btn btn-primary">Сохранить изменения</button>
        </form>
    </div>

    <div class="row mb-5">
      <div class="col-md-6 text-center">
        <h4 class="text-center">Qr-код на сайт</h4>
        <QRCodeVue3
          ref="qrCodeLeft"
          :value="qr_code"
          :width="200"
          :height="200"
          :qrOptions="{ typeNumber: '0', mode: 'Byte', errorCorrectionLevel: 'Q' }"
          :imageOptions="{ hideBackgroundDots: true, imageSize: 0.4, margin: 0 }"
          :dotsOptions="{ type: 'square', color: '#000000' }"
          :cornersSquareOptions="{ type: 'square', color: '#000000' }"

           fileExt="png"
          :download="true"
          downloadButton="btn btn-primary mt-2"
          :downloadOptions="{ name: 'vqr', extension: 'png' }"
        />
      </div>
      <div class="col-md-6 text-center">
        <h4 class="text-center">Qr-код в telegram</h4>
        <QRCodeVue3
          ref="qrCodeRight"
          :value="tg_qr_code"
          :width="200"
          :height="200"
          :qrOptions="{ typeNumber: '0', mode: 'Byte', errorCorrectionLevel: 'Q' }"
          :imageOptions="{ hideBackgroundDots: true, imageSize: 0.4, margin: 0 }"
          :dotsOptions="{ type: 'square', color: '#000000' }"
          :cornersSquareOptions="{ type: 'square', color: '#000000' }"

           fileExt="png"
          :download="true"
          downloadButton="btn btn-primary mt-2"
          :downloadOptions="{ name: 'vqr', extension: 'png' }"
        />
      </div>
    </div>
</template>

<script>
import axios from 'axios';
import QRCodeVue3 from "qrcode-vue3";

export default {
  name: 'device_edit',
  components: {
    QRCodeVue3
  },
  data() {
    return {
      qr_code: 'http://localhost:8080/create_problem/' + this.$route.params.id,
      tg_qr_code: `https://t.me/${'tg_dpns_bot'}?start=id`,

      device_id: this.$route.params.id,
      device_name: '',
      device_type: '',
      device_description: '',
      building: '',
      floor: '',
      room: '',
      location_description: '',
    };
  },
  async created() {
     axios.defaults.withCredentials = true;
     console.log(`https://t.me/${'tg_dpns_bot'}?start=id${this.device_id}`);
     this.tg_qr_code = `https://t.me/${'tg_dpns_bot'}?start=${this.device_id}`;
    try {
      const response = await axios.get(`${this.$urlServer}/devices/get?device_id=${this.device_id}`);
      const deviceData = response.data;
      this.device_name = deviceData.name;
      this.device_type = deviceData.type_device;
      this.building = deviceData.building;
      this.floor = deviceData.floor;
      this.room = deviceData.room;
      this.device_description = deviceData.description;
      this.location_description = deviceData.location_description;
      console.log(deviceData);
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
    async updateDevice(){
        event.preventDefault();
        try {
          const params = new URLSearchParams({
            device_id: this.device_id,
            description: this.device_description,
            building: this.building,
            floor: this.floor,
            room: this.room,
            location_description: this.location_description
          });
          const response = await axios.post(`${this.$urlServer}/devices/update?${params.toString()}`,);
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
