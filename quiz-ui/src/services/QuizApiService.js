import axios from "axios";
import participationStorageService from "@/Services/ParticipationStorageService";

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}`,
  json: true
});

export default {
  async call(method, resource, data = null) {
    const token = participationStorageService.getToken();
    var headers = {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    };

    return instance({
      method,
      headers: headers,
      url: resource,
      data,
    })
      .then((response) => {
        return { status: response.status, data: response.data };
      })
      .catch((error) => {
        console.error(error);
      });
  },
  getQuizInfo() {
    return this.call("get", "quiz-info");
  },
  getQuestions() {
    return this.call("get", "questions/get_all");
  },

  getQuestionById(questionId) {
    return this.call("get", `questions/${questionId}`);
  },

  removeQuestion(questionId) {
    return this.call("delete", `questions/${questionId}`);
  },


  async login(password) {
    try {
      const response = await this.call("post", "login", {
        password
      });
      return response;
    } catch (error) {
      console.error(error);
    }
  },
  

  async saveScore(playerName, answers) {
    try {
      const response = await this.call("post", "participations", {
        playerName,
        answers
      });
      return response;
    } catch (error) {
      console.error(error);
    }
  },
  async addQuestion(questionData) {
    try {
      const response = await this.call("post", "questions", {
        ...questionData,
        headers: {
          "Content-Type": "application/json"
        }
      });
      return response;
    } catch (error) {
      console.error(error);
    }
  },

  async editQuestion(questionId, questionData) {
    try {
      const response = await this.call("put", `questions/${questionId}`, {
        ...questionData,
        headers: {
          "Content-Type": "application/json"
        }
      });
      return response;
    } catch (error) {
      console.error(error);
    }
  }
  
};

//intro
//thread
//processus
//interblocage
//inter process synchro
//gestion memoire
//system fichier
