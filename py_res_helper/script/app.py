import asyncio
import pyperclip
import psutil
from res_script import ResumeHelper
from playwright_script import PlaywrightHelper, AIList


def force_kill_browser():
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] in ["chrome.exe", "chromium.exe"]:
            try:
                proc.kill()
            except psutil.NoSuchProcess:
                pass


# This guard is required for multiprocessing to work
res_helper = ResumeHelper()


async def run_multi_playwright():

    playwright_helper = PlaywrightHelper()

    playwright_helper1 = PlaywrightHelper("1")

    playwright_helper2 = PlaywrightHelper("2")

    tasks = [
        playwright_helper.ai_to_run_driver(AIList.CHATGPT.value),
        playwright_helper1.ai_to_run_driver(AIList.META_AI.value),
        playwright_helper2.ai_to_run_driver(AIList.COPILOT.value),
    ]
    await asyncio.gather(*tasks)

    return [playwright_helper, playwright_helper1, playwright_helper2]


# async def close_all_browsers(helpers):
#     if helpers:
#         await asyncio.gather(*(helper.close_browser() for helper in helpers))


async def main():
    helpers = None
    run = True
    while run:
        if helpers:
            for helper in helpers:
                asyncio.run(helper.close_browser())

        force_kill_browser()

        helpers_task = asyncio.create_task(run_multi_playwright())

        res_helper.default_resume_path()

        designaion = res_helper.get_programmer_title()

        date_now = res_helper.get_formated_date()

        # Resume Workings
        res_helper.replace_string_in_word_table(
            search_text="date",
            replacement_text=date_now,
            file=res_helper.resume_template,
            save_location=res_helper.resume_output,
            irow=4,
            icell=1,
        )

        res_helper.replace_string_word(
            search_text="designation",
            replacement_text=designaion,
            file=res_helper.resume_output,
            save_location=res_helper.resume_output,
        )

        input("\n\nPlease Copy Contents of Job Description and Press Enter ")

        job_description = res_helper.format_data(pyperclip.paste())

        res_helper.replace_string_word(
            search_text="job_description",
            replacement_text=job_description,
            file=res_helper.resume_output,
            save_location=res_helper.resume_output,
        )

        # Copies the Data to the memory
        res_helper.copy_keyword_job_resume(
            res_helper.resume_summary_template, job_description
        )

        helpers = await helpers_task

        input("\n\n✅ Please Copy The Summary and Press Enter ")

        res_helper.replace_string_word(
            search_text="summary_placeholder",
            replacement_text=pyperclip.paste(),
            file=res_helper.resume_output,
            save_location=res_helper.resume_output,
        )

        res_helper.launch_file(res_helper.resume_output)

        input("\n\nPress Enter Generate Resume PDF")

        res_helper.generate_pdf(res_helper.resume_output, res_helper.resume_pdf)

        # Cover Leter
        res_helper.replace_string_word(
            search_text="designation",
            replacement_text=designaion,
            file=res_helper.cover_letter_template,
            save_location=res_helper.cover_letter_output,
        )

        res_helper.replace_string_word(
            search_text="date",
            replacement_text=date_now,
            file=res_helper.cover_letter_output,
            save_location=res_helper.cover_letter_output,
        )

        input("\n\nPress Enter, Cover Body On The Word Template ")

        body_text = res_helper.replace_lines_breaks(pyperclip.paste())

        input("\n\nPress Enter To Copy the Company Name On The Word Template ")

        company_name_to_replace = res_helper.extract_company_name(pyperclip.paste())

        if company_name_to_replace:
            body_text = body_text.replace("[Company Name]", company_name_to_replace)

        company_name = res_helper.format_text_single_break(pyperclip.paste())

        res_helper.replace_string_word(
            search_text="body",
            replacement_text=body_text,
            file=res_helper.cover_letter_output,
            save_location=res_helper.cover_letter_output,
        )

        res_helper.replace_string_word(
            search_text="company_name",
            replacement_text=company_name,
            file=res_helper.cover_letter_output,
            save_location=res_helper.cover_letter_output,
            isbold=True,
        )
        contact_person = res_helper.format_data(
            input("\n\n⚠️  Enter a Contact Person Manually ")
        )
        if contact_person:
            res_helper.replace_string_word(
                search_text="Hiring Manager",
                replacement_text=contact_person,
                file=res_helper.cover_letter_output,
                save_location=res_helper.cover_letter_output,
                isbold=False,
            )
        else:
            contact_person = "Hiring Manager"

        res_helper.launch_file(res_helper.cover_letter_output)

        input("\n\nPress Enter To Generate Cover Letter ")

        res_helper.generate_pdf(
            res_helper.cover_letter_output, res_helper.cover_letter_pdf
        )

        res_helper.merge_pdfs(
            res_helper.cover_letter_pdf,
            res_helper.resume_pdf,
            res_helper.resume_cover_merge,
        )

        res_helper.copy_word_to_txt(
            res_helper.cover_letter_output, res_helper.cover_letter_txt
        )

        res_helper.add_row_to_excel(
            res_helper.job_tracker_xls,
            [
                company_name,
                designaion,
                contact_person,
                date_now,
                job_description,
            ],
        )

        # res_helper.launch_file(res_helper.job_tracker_xls)

        continue_run = input(
            """
        \n\nAll Operations are Completed\n
        ---------------------------------
        |                               |
        |   Script execution complete   |
        |                               |
        ---------------------------------
        \n\nPress Enter to Start Again...
        """
        )

    if continue_run == "1":
        run = False


asyncio.run(main())
