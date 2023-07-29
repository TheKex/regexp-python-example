from pprint import pprint
import csv
import re


def format_fio(lastname, firstname, surname):
    full_fio = (lastname + ' ' + firstname + ' ' + surname).strip()
    return full_fio.split()


def format_phone(phone):
    phone_pattern = r"(\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})"
    phone_format_pattern = r"+7(\2)\3-\4-\5"
    phone = re.sub(phone_pattern, phone_format_pattern, phone)

    add_phone_pattern = r"(\s*\(?(доб)\.\s*(\d+)\.?\)?)"
    add_phone_format_pattern = r" \2.\3."
    phone = re.sub(add_phone_pattern, add_phone_format_pattern, phone)
    return phone


def contain_contact(contact, contacts_list):
    index = -1
    for i, cont in enumerate(contacts_list):
        if cont[0] == contact[0] and cont[1] == contact[1]:
            index = i
            break
    return index


def delete_duplicates(contacts_list):
    result = []
    for cont in contacts_list:
        index = contain_contact(cont, result)
        if index == -1:
            result.append(cont)
        else:
            result[index] = list(map(lambda x, y: x or y, result[index], cont))
    return result


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    for contact in contacts_list:
        fio = format_fio(*contact[0:3])
        for i in range(3):
            contact[i] = fio[i] if len(fio) > i else ""

        contact[5] = format_phone(contact[5])

    contacts_list = delete_duplicates(contacts_list)

    with open("phonebook.csv", "w", encoding='utf-8', newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)

