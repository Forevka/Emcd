<template>
  <div v-if="isLoaded">
    Broadcasts management
    <div
      class="card align-items-left text-left"
      :class="{
        'border-success': b.statusId === 3,
        'border-warning': b.statusId === 2,
        }"
      v-for="b in broadcasts"
      :key="b.id"
    >
      <div class="card-body d-flex justify-content-start">
        <div class="organisation align-self-center">
          <div class="status font-weight-bold text-center align-middle">
            {{ getStatusName(b.statusId) }} #{{ b.id }}
          </div>
          <div class="planned-datetime border text-center align-middle">
            <datepicker v-model="b.startDatetime" v-if="b.statusId === 1"/>
            <div v-else>
              {{ formatDate(b.startDatetime) }}
            </div>
            <div>
              {{ formatTime(b.startDatetime) }}
            </div>
          </div>
        </div>
        <div class="langs">
          <ul
            class="nav nav-pills nav-fill"
            :id="`tabLang-${b.id}`"
            :role="`tablist-${b.id}`"
          >
            <li class="nav-item" v-for="l in langs" :key="l.id">
              <a
                class="nav-link"
                :class="{
                  active: broadcastsChosenLang[b.id] === l.id
                }"
                @click="changeLangTab(b.id, l.id)"
                >{{ langById(l.id).name || 'Unknown lang' }} 
                    <i :class="{
                        'fa fa-check': b.data.find((x) => x.langId === l.id) !== undefined,
                        'fa fa-times': b.data.find((x) => x.langId === l.id) === undefined,
                    }" aria-hidden="true"></i>
                </a
              >
            </li>
          </ul>
          <div class="broadcast-lang-text border" @click="openBroadcastEditModal($event, b.id)">
            {{textByLangId(b.id)?.text || 'Text not defined'}}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { formatDate, formatTime } from "@/utils/formatDate";
import { showLoader, hideLoader } from "@/utils/loader";
import { ActionTypes as UserActions } from "@/store/user/actions";
import { Lang } from "@/models/Lang";
import { emitter } from '@/utils/bus';
import {notification} from '@/utils/notification';

@Options({
  components: {}
})
export default class Broadcast extends Vue {
  isLoaded = false;

    openBroadcastEditModal(event: any, broadcastId: number,) {
        console.log(event)
        const qq = this.broadcasts.find((x) => x.id === broadcastId)
        if (qq) {
            if (qq.statusId !== 1) {
                notification.warning({
                    message: `You cant change text for broadcasts that in ${this.getStatusName(qq.statusId).toLowerCase()} status`
                })

                return;
            }
            
            // @ts-ignore
            window.$('#broadcastEditModal').modal('show')

            emitter.emit('broadcastEditModalOpen', {
                broadcastId: qq.id,
                langId: this.broadcastsChosenLang[broadcastId],
                text: this.textByLangId(broadcastId)?.text,
            })
        }
    }

    changeLangTab(broadcastId: number, langId: number) {
        this.broadcastsChosenLang[broadcastId] = langId
    }

  formatDate(date: Date) {
    return formatDate(date);
  }

  formatTime(date: Date) {
    return formatTime(date);
  }

  getStatusName(statusId: number) {
    const statuses: { [key: number]: string } = {
      1: "Planned",
      2: "Processing",
      3: "Done"
    };

    return statuses[statusId];
  }

  broadcastsChosenLang: { [key: number]: number } = {
    1: 1,
    2: 3,
    3: 2
  };

  broadcasts = [
    {
      id: 1,
      createdDatetime: new Date(2021, 10, 11),
      startDatetime: new Date(2021, 10, 12, 12, 30, 0),
      statusId: 1,
      data: [
        {
          langId: 1,
          text: "Тест"
        },
        {
          langId: 2,
          text: "Hello"
        }
      ]
    },
    {
      id: 2,
      createdDatetime: new Date(2021, 9, 11),
      startDatetime: new Date(2021, 9, 12),
      statusId: 2,
      data: [
        {
          langId: 1,
          text: "Тест"
        },
        {
          langId: 2,
          text: "Hello"
        },
        {
          langId: 3,
          text: "ohayo"
        }
      ]
    },
    {
      id: 3,
      createdDatetime: new Date(2021, 9, 11),
      startDatetime: new Date(2021, 9, 12),
      statusId: 3,
      data: [
        {
          langId: 1,
          text: "Тест"
        },
        {
          langId: 2,
          text: "Hello"
        },
        {
          langId: 3,
          text: "qweqwwqwe"
        }
      ]
    }
  ];

  async created() {
    this.isLoaded = false;

    if (this.langs.length === 0) {
      showLoader();
      await this.$store.dispatch(UserActions.UPDATE_LANGS).then(() => {
        hideLoader();
        this.isLoaded = true;
      });
    } else {
      this.isLoaded = true;
    }
  }

    textByLangId(broadcastId: number) {
        const br = this.broadcasts.find((x) => x.id === broadcastId)
        return br?.data.find((x) => x.langId === this.broadcastsChosenLang[broadcastId])
    }

  langById(langId: number) {
    return this.langs.filter(x => x.id == langId)[0];
  }

  get langs(): Lang[] {
    return this.$store.getters.getLangs;
  }
}
</script>

<style lang="scss" scoped>
a {
  cursor: pointer;
}

.card {
  margin: 1rem;
}

.langs {
  width: -webkit-fill-available;
  display: flex;
  flex-flow: column;
}

.organisation {
  max-width: 15%;
  min-width: 15%;

  .status {
    font-size: 1em;
    min-height: 4rem;
  }

  .planned-datetime {
    min-height: 4rem;
  }
}

.broadcast-lang-text {
    margin: 0.5rem;
    padding: 0.5rem;
    margin-bottom: 0;
    background-color: #f5f5f5;
    flex: 1 1 auto;

    &:hover {
        border: 1px solid #585a61!important;
    }
}
</style>