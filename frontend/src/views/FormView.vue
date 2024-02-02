<script setup>
import { ref } from 'vue';

const formData = ref({
  name: '',
  email: '',
  age: null,
});

const successMessage = ref('');
const errorMessage = ref('');
let response = {};

const handleSubmit = async () => {

    try {
       response = await sendFormDataToBackend(formData.value);

      // Handle success response
      if (response.success) {
        successMessage.value = 'Form submitted successfully!';
        resetForm();
      } else {
        // Handle failure response
        errorMessage.value = 'Form submission failed. Please check the following fields:';
        // Display the specific fields that failed and their errorText
      }
    } catch (error) {
      console.error('Error submitting form:', error);
      errorMessage.value = 'An error occurred while submitting the form.';
    }
};

const resetForm = () => {
  formData.value = {
    name: '',
    email: '',
    age: null,
  };
};


const sendFormDataToBackend = async (formData) => {
  try {
    const apiUrl = 'http://localhost:3000/payhealth';
    const response = await fetch(apiUrl, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }
    return response.json();
  } catch (error) {
    console.error('Error sending form data to backend:', error);
    throw error;
  }
};

const isFieldInvalid = (fieldName) => {
  return (
      errorMessage.value &&
      response[0].validations.some(validation => validation.field === `FIELD_${fieldName}` && validation.success === 'false')
  );
};

const getErrorText = (fieldName) => {
  const fieldError = response[0].validations.find(validation => validation.field === `FIELD_${fieldName}`);
  return fieldError ? fieldError.errorText : '';
};
</script>

<template>
  <div class="center-box">
    <div class="form-box">
      <form @submit.prevent="handleSubmit">
        <div class="form-group" :class="{ 'has-error': isFieldInvalid('NAME') }">
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="formData.name" required />
          <div v-if="isFieldInvalid('NAME')" class="error-text">{{ getErrorText('NAME') }}</div>
        </div>
        <div class="form-group" :class="{ 'has-error': isFieldInvalid('EMAIL') }">
          <label for="email">Email:</label>
          <input type="text" id="email" v-model="formData.email" required />
          <div v-if="isFieldInvalid('EMAIL')" class="error-text">{{ getErrorText('EMAIL') }}</div>
        </div>
        <div class="form-group" :class="{ 'has-error': isFieldInvalid('AGE') }">
          <label for="age">Age:</label>
          <input type="text" id="age" v-model="formData.age" required />
          <div v-if="isFieldInvalid('AGE')" class="error-text">{{ getErrorText('AGE') }}</div>
        </div>
        <button type="submit">Submit</button>
      </form>

      <div v-if="successMessage" class="success-message">
        {{ successMessage }}
      </div>

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.center-box {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.form-box {
  width: 300px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  background-color: #4caf50;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.success-message {
  color: #4caf50;
  margin-top: 10px;
}

.error-message {
  color: #ff5722;
  margin-top: 10px;
}

.form-group.has-error {
  border: 1px solid #ff5722;
}

.error-text {
  color: #ff5722;
  margin-top: 5px;
  font-size: 12px;
}
</style>