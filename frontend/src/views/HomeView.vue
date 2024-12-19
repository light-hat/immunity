<template>
    <div class="uk-container uk-container-expand uk-position-center">
        <div class="uk-child-width-1-3@m uk-grid-small uk-grid-match" uk-grid>

            <div>
                <div class="uk-card uk-card-default uk-card-hover uk-card-body">
                    <h3 class="uk-card-title">
                        Типы уязвимостей в приложениях
                    </h3>
                    <ag-charts :options="options"/>
                </div>
            </div>

            <div>
                <div class="uk-card uk-card-default uk-card-hover uk-card-body">
                    <h3 class="uk-card-title">Default</h3>
                    <ag-charts :options="options"/>
                </div>
            </div>

            <div>
                <div class="uk-card uk-card-default uk-card-hover uk-card-body">
                    <h3 class="uk-card-title">Primary</h3>
                    <ag-charts :options="options"/>
                </div>
            </div>

            <div>
                <div class="uk-card uk-card-default uk-card-hover uk-card-body">
                    <h3 class="uk-card-title">Secondary</h3>
                    <ag-charts :options="options"/>
                </div>
            </div>

            <div>
                <div class="uk-card uk-card-default uk-card-hover uk-card-body">
                    <h3 class="uk-card-title">Secondary</h3>
                    <ag-charts :options="options"/>
                </div>
            </div>

            <div>
                <div class="uk-card uk-card-default uk-card-hover uk-card-body">
                    <h3 class="uk-card-title">Secondary</h3>
                    <ag-charts :options="options"/>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
import {ref} from 'vue';

import {AgCharts} from 'ag-charts-vue3';

export default {
  name: 'App',
  components: {
    'ag-charts': AgCharts,
  },
  setup() {
    const options = ref({
      data: [
        {month: 'Jan', avgTemp: 2.3, iceCreamSales: 162000},
        {month: 'Mar', avgTemp: 6.3, iceCreamSales: 302000},
        {month: 'May', avgTemp: 16.2, iceCreamSales: 800000},
        {month: 'Jul', avgTemp: 22.8, iceCreamSales: 1254000},
        {month: 'Sep', avgTemp: 14.5, iceCreamSales: 950000},
        {month: 'Nov', avgTemp: 8.9, iceCreamSales: 200000},
      ],
      series: [{type: 'bar', xKey: 'month', yKey: 'iceCreamSales'}],
    });
    return {
      options,
    };
  },
};
</script>
