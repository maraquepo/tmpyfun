<script setup lang="ts">
import { h, ref } from "vue";
import {
  useVueTable,
  getCoreRowModel,
  FlexRender,
  getPaginationRowModel,
  getSortedRowModel,
  getFilteredRowModel,
} from "@tanstack/vue-table";
import { format } from "date-fns";
import EditButton from "./EditButton.vue";
import { useQuery } from "@tanstack/vue-query";
import { getUsers } from "../../services/apiClient.ts";
import { onMounted } from "vue";

const queryData = ref([]);

// Define an asynchronous function to fetch people data
const fetchPeople = async () => {
  try {
    // Fetch data from the API
    const response = await getUsers();

    // Parse the JSON response

    queryData.value = response.data;
  } catch (error) {
    console.error("Error fetching people data:", error);
  }
};

// Call fetchPeople function when the component is mounted
onMounted(fetchPeople);

const columnsPeople = [
  {
    accessorKey: "fullname", // Assuming the ID is the first element
    header: "Full Name",
  },
  {
    accessorKey: "email",
    header: "Email",
  },
  {
    accessorKey: "createdAt",
    header: "Created At",
    cell: (info) => format(new Date(info.getValue()), "MMM d, yyyy"),
  },
  {
    accessorKey: "updatedAt",
    header: "Updated At",
    cell: (info) => format(new Date(info.getValue()), "MMM d, yyyy"),
  },
  {
    accessorKey: "picture",
    header: "Picture",
    enableResizing: true,
  },
  {
    accessorKey: "tokenBalance",
    header: "Token Balance",
  },
  // {
  //   accessorKey: "public_user_id",
  //   header: "Public User ID",
  // },
  // {
  //   accessorKey: "creator_user_id", // Name
  //   header: "Creator User ID",
  // },
  // {
  //   accessorKey: "passwordhash",
  //   header: "Password Hash",
  // },
  // {
  //   accessorKey: "signupIP",
  //   header: "Signup IP",
  // },
  // {
  //   accessorKey: "institution",
  //   header: "Instituiton",
  // },
  // {
  //   accessorKey: "bio",
  //   header: "Bio",
  // },
  {
    accessorKey: "id",
    header: "ID",
  },
  {
    accessorKey: "edit",
    header: " ",
    cell: ({ row }) =>
      h(EditButton, { id: row.original.id, rowData: row.original }),
  },
];

const sorting = ref([]);
const filter = ref("");

const table = useVueTable({
  get data() {
    return queryData.value;
  },
  columns: columnsPeople,
  getCoreRowModel: getCoreRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
  state: {
    get sorting() {
      return sorting.value;
    },
    get globalFilter() {
      return filter.value;
    },
  },
  onSortingChange: (updaterOrValue) => {
    sorting.value =
      typeof updaterOrValue === "function"
        ? updaterOrValue(sorting.value)
        : updaterOrValue;
  },
  // initialState: {
  //   pagination: {
  //     pageSize: 10,
  //   },
  // },
});
</script>

<script lang="ts">
export default {
  name: "PeopleTable",
};
</script>

<template>
  <div class="px-4 sm:px-6">
    <div class="mt-8 flow-root">
      <div class="-mx-4 -my-2 sm:-mx-6 lg:-mx-8">
        <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
          <div class="my-4">
            <input
              type="text"
              class="border border-gray-400 rounded px-2 py-2"
              placeholder="Search"
              v-model="filter"
            />
          </div>
          <table class="min-w-full divide-y divide-gray-300">
            <thead>
              <tr
                v-for="headerGroup in table.getHeaderGroups()"
                :key="headerGroup.id"
              >
                <th
                  v-for="header in headerGroup.headers"
                  :key="header.id"
                  scope="col"
                  class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900"
                  :class="{
                    'cursor-pointer select-none': header.column.getCanSort(),
                    'w-20': header.column.id === 'picture', // Adjust width as per your requirement
                  }"
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
                  class="whitespace-nowrap px-3 py-4 text-sm text-gray-500"
                  :class="{
                    'w-20': cell.column.id === 'picture', // Adjust width as per your requirement
                  }"
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
      <div class="mt-8">
        Page {{ table.getState().pagination.pageIndex + 1 }} of
        {{ table.getPageCount() }} -
        {{ table.getFilteredRowModel().rows.length }} results
      </div>
      <div class="mt-8 space-x-4">
        <button
          class="border border-gray-300 rounded px-2 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
          @click="table.setPageSize(5)"
        >
          Page Size 5
        </button>
        <button
          class="border border-gray-300 rounded px-2 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
          @click="table.setPageSize(10)"
        >
          Page Size 10
        </button>
        <button
          class="border border-gray-300 rounded px-2 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
          @click="table.setPageSize(20)"
        >
          Page Size 20
        </button>
      </div>
      <div class="space-x-4 mt-8">
        <button
          class="border border-gray-300 rounded px-2 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
          @click="table.setPageIndex(0)"
        >
          First page
        </button>
        <button
          class="border border-gray-300 rounded px-2 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
          @click="table.setPageIndex(table.getPageCount() - 1)"
        >
          Last page
        </button>
        <button
          class="border border-gray-300 rounded px-2 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="!table.getCanPreviousPage()"
          @click="table.previousPage()"
        >
          Prev page
        </button>
        <button
          class="border border-gray-300 rounded px-2 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="!table.getCanNextPage()"
          @click="table.nextPage()"
        >
          Next page
        </button>
      </div>
    </div>
  </div>
</template>
