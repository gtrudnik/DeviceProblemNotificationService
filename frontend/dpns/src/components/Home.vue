<template>
    <div class="container text-center mt-5">
        <h1 class="display-4">DPNS</h1>
        <p class="lead mt-4">
            DPNS - (device problem notification service) это сервис оповещения о проблемах на устройствах. Например, есть принтер и с ним возникла какая-либо проблема, Вы сканируете qr-код и переходите на этот сайт или в телеграмм бота, затем заполняете форму, и заявка о проблеме придёт администраторам. В личном кабинете можно отслеживать Ваши заявки. Также можно получить уведомление о готовности в телеграмм, если он будет привязан к Вашему аккаунту (или если изначально заявка подавалась через телеграмм бота).
        </p>
        <a href="/auth_form" class="btn btn-primary btn-lg mt-4">Войти</a>
    </div>
</template>

<script>

export default {
  name: 'homePage',
  data() {
    return {
      email: '',
      password: ''
    };
  },
};
</script>

<style scoped>
.container {
  margin-top: 100px;
}
</style>