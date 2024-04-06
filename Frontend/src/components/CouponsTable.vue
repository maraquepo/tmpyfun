<script setup lang="ts">
import { h, ref, onMounted, watch } from "vue";
import {
  useVueTable,
  getCoreRowModel,
  FlexRender,
  getPaginationRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  RowSelection,
  type RowSelectionState,
} from "@tanstack/vue-table";
import CheckBox from "./CheckBox.vue";
import EditButtonTwo from "./EditButtonTwo.vue";
import { format } from "date-fns";
import { getCoupons } from "../../services/apiClient.ts";

const queryData = ref([]);
const dataFetched = ref(false);

const fetchCoupons = async () => {
  try {
    const res = await getCoupons();
    queryData.value = res.data;
    dataFetched.value = true;
  } catch (err) {
    console.error("Error fetching coupons data:", err);
  }
};

onMounted(() => {
  if (!dataFetched.value) {
    fetchCoupons();
  }
});

const columnsTeams = [
  {
    accessorKey: "promo_code",
    header: "Coupon Name",
  },
  {
    accessorKey: "description",
    header: "Description",
  },
  {
    accessorKey: "number_of_tokens",
    header: "Amount",
  },
  {
    accessorKey: "clicked_count",
    header: "Clicks",
  },
  {
    accessorKey: "creation_date",
    header: "Created At",
    cell: (info) => format(new Date(info.getValue()), "MMM d, yyyy"),
    sortType: "datetime",
  },
  {
    accessorKey: "expiration_date",
    header: "Expired At",
    cell: (info) => format(new Date(info.getValue()), "MMM d, yyyy"),
    sortType: "datetime",
  },
  {
    accessorKey: "edit",
    header: " ",
    cell: ({ row }) =>
      h(EditButtonTwo, {
        id: row.original.id,
        rowData: row.original,
        fetchItems: fetchCoupons,
      }),
  },
];

const sorting = ref([]);
const filter = ref("");
const rowSelection = ref<RowSelectionState>({});

const table = useVueTable({
  get data() {
    return queryData.value;
  },
  columns: columnsTeams,
  getCoreRowModel: getCoreRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
  enableRowSelection: true,
  initialState: {
    rowSelection: rowSelection.value,
    pagination: {
      pageSize: 7,
    },
  },
  state: {
    get sorting() {
      return sorting.value;
    },
    get globalFilter() {
      return filter.value;
    },
    get rowSelection() {
      return rowSelection.value;
    },
  },
  onSortingChange: (updaterOrValue) => {
    sorting.value =
      typeof updaterOrValue === "function"
        ? updaterOrValue(sorting.value)
        : updaterOrValue;
  },
  onRowSelectionChange: (updateOrValue) => {
    rowSelection.value =
      typeof updateOrValue === "function"
        ? updateOrValue(rowSelection.value)
        : updateOrValue;
  },
});
</script>

<template>
  <div class="px-4 sm:px-6">
    <div class="block">
      <div class="-mx-4 -my-2 sm:-mx-6 lg:-mx-8">
        <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
          <div class="my-1 flex">
            <input
              type="text"
              class="border border-gray-400 rounded px-2 py-2"
              placeholder="Search"
              v-model="filter"
            />
            <div v-if="Object.keys(rowSelection).length !== 0" class="px-2">
              <EditOrDeleteModalTwo
                :teams="table.getSelectedRowModel().flatRows"
                :fetch-coupons="fetchCoupon"
              />
            </div>
          </div>
          <table class="w-full text-left divide-y divide-gray-300">
            <thead>
              <tr
                v-for="headerGroup in table.getHeaderGroups()"
                :key="headerGroup.id"
              >
                <th
                  v-for="header in headerGroup.headers"
                  :key="header.id"
                  scope="col"
                  class="px-3 py-3.5 text-left text-sm font-semibold text-green-400"
                  @click="header.column.getToggleSortingHandler()?.($event)"
                >
                  <FlexRender
                    :render="header.column.columnDef.header"
                    :props="header.getContext()"
                  />
                  {{ { asc: " ↑", desc: "↓" }[header.column.getIsSorted()] }}
                </th>
              </tr>
            </thead>

            <tbody class="divide-y divide-gray-200">
              <tr v-for="row in table.getRowModel().rows" :key="row.id">
                <td
                  v-for="cell in row.getVisibleCells()"
                  :key="cell.id"
                  class="px-3 py-4 text-sm text-ellipsis text-gray-500 overflow-hidden"
                >
                  <FlexRender
                    :render="cell.column.columnDef.cell"
                    :props="cell.getContext()"
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div class="mt-8 text-green-400">
        Page {{ table.getState().pagination.pageIndex + 1 }} of
        {{ table.getPageCount() }} -
        {{ table.getFilteredRowModel().rows.length }} results
      </div>
      <div class="mt-8 space-x-4">
        <button
          class="border border-green-400 rounded px-2 py-2 disabled:opacity-50 disabled:cursor-not-allowed text-green-400"
          @click="table.setPageSize(5)"
        >
          Page Size 5
        </button>
        <button
          class="border border-green-400 text-green-400 rounded px-2 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
          @click="table.setPageSize(10)"
        >
          Page Size 10
        </button>
        <button
          class="border border-green-400 text-green-400 rounded px-2 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
          @click="table.setPageSize(20)"
        >
          Page Size 20
        </button>
      </div>
      <div class="space-x-4 mt-8">
        <button
          class="border border-green-400 text-green-400 rounded px-2 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
          @click="table.setPageIndex(0)"
        >
          First page
        </button>
        <button
          class="border border-green-400 text-green-400 rounded px-2 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
          @click="table.setPageIndex(table.getPageCount() - 1)"
        >
          Last page
        </button>
        <button
          class="border border-green-400 text-green-400 rounded px-2 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="!table.getCanPreviousPage()"
          @click="table.previousPage()"
        >
          Prev page
        </button>
        <button
          class="border border-green-400 text-green-400 rounded px-2 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="!table.getCanNextPage()"
          @click="table.nextPage()"
        >
          Next page
        </button>
      </div>
    </div>
  </div>
</template>
