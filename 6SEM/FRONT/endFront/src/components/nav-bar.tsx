import { Link, Outlet } from "react-router-dom";
import { Sheet, SheetContent, SheetTrigger } from "./ui/sheet";
import { CircleUser, Menu, Package2, Search } from "lucide-react";
import { Button } from "./ui/button";

import { Input } from "./ui/input";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "./ui/dropdown-menu";

const NavBar = () => {
  return (
    <div className="flex min-h-screen w-full flex-col">
      <header className="sticky top-0 flex h-16 items-center gap-4 border-b bg-background px-4 md:px-6 dark:border-b-zinc-700 z-50">
        <nav className="hidden flex-col gap-6 text-lg font-medium md:flex md:flex-row md:items-center md:gap-5 md:text-sm lg:gap-6">
          <Link
            to="#"
            className="flex items-center gap-2 text-lg font-semibold md:text-base"
          >
            <Package2 className="h-6 w-6" />
            <span className="sr-only">Politrium Limited</span>
          </Link>
          <Link
            to="/dashboard"
            className="text-foreground transition-colors hover:text-foreground"
          >
            Главная
          </Link>
          <Link
            to="#"
            className="text-muted-foreground transition-colors hover:text-foreground"
          >
            Заказы
          </Link>
          <Link
            to="/dashboard/products"
            className="text-muted-foreground transition-colors hover:text-foreground"
          >
            Товары
          </Link>
          <Link
            to="#"
            className="text-muted-foreground transition-colors hover:text-foreground"
          >
            Клиенты
          </Link>
          <Link
            to="#"
            className="text-muted-foreground transition-colors hover:text-foreground"
          >
            Аналитика
          </Link>
        </nav>
        <Sheet>
          <SheetTrigger asChild>
            <Button
              variant="outline"
              size="icon"
              className="shrink-0 md:hidden"
            >
              <Menu className="h-5 w-5" />
              <span className="sr-only">Открыть меню навигации</span>
            </Button>
          </SheetTrigger>
          <SheetContent side="left">
            <nav className="grid gap-6 text-lg font-medium">
              <Link
                to="#"
                className="flex items-center gap-2 text-lg font-semibold"
              >
                <Package2 className="h-6 w-6" />
                <span className="sr-only">Politrium Limited</span>
              </Link>
              <Link to="/dashboard" className="hover:text-foreground">
                Главная
              </Link>
              <Link
                to="#"
                className="text-muted-foreground hover:text-foreground"
              >
                Заказы
              </Link>
              <Link
                to="/dashboard/products"
                className="text-muted-foreground hover:text-foreground"
              >
                Товары
              </Link>
              <Link
                to="#"
                className="text-muted-foreground hover:text-foreground"
              >
                Клиенты
              </Link>
              <Link
                to="#"
                className="text-muted-foreground hover:text-foreground"
              >
                Аналитика
              </Link>
            </nav>
          </SheetContent>
        </Sheet>
        <div className="flex w-full items-center gap-4 md:ml-auto md:gap-2 lg:gap-4">
          <form className="ml-auto flex-1 sm:flex-initial">
            <div className="relative">
              <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input
                type="search"
                placeholder="Поиск товаров..."
                className="pl-8 sm:w-[300px] md:w-[200px] lg:w-[300px]"
              />
            </div>
          </form>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="secondary" size="icon" className="rounded-full">
                <CircleUser className="h-5 w-5" />
                <span className="sr-only">Открыть меню пользователя</span>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuLabel>Мой аккаунт</DropdownMenuLabel>
              <DropdownMenuSeparator />
              <DropdownMenuItem>Настройки</DropdownMenuItem>
              <DropdownMenuItem>Поддержка</DropdownMenuItem>
              <DropdownMenuSeparator />
              <DropdownMenuItem>Выход</DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
      </header>
      <main className="flex flex-1 flex-col gap-4 p-4 md:gap-8 md:p-8">
        <Outlet />
      </main>
    </div>
  );
};

export default NavBar;
